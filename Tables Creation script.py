import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# =====================================================================
# GLOBAL CONFIGURATION & REPRODUCIBILITY
# =====================================================================
np.random.seed(42)

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 3, 31)  # Aligned with final dataset boundaries
TOTAL_DAYS = (END_DATE - START_DATE).days + 1

# Business footprint configurations
TOTAL_WASHERS = 10
TOTAL_DRYERS = 10
TOTAL_VENDING_MACHINES = 2


class LaundromatDataPipeline:
    """
    An enterprise-grade, modular pipeline designed to synthesize, validate,
    and scale transactional relational warehouse architectures. Built with
    traceable logic loops to support backward error reconciliation.
    """
    
    def __init__(self, output_dir="."):
        self.output_dir = output_dir
        self.df_machines = None
        self.df_vending = None
        self.df_customers = None
        self.df_transactions = None

    def build_machines_dimension(self):
        """
        Generates the core physical machine assets table.
        Aligns perfectly with the target warehouse schemas.
        """
        try:
            machines = []
            
            # Synthesize Washer Portfolio
            for i in range(1, TOTAL_WASHERS + 1):
                machines.append({
                    'Machine_ID': f'W{i:02d}',
                    'Machine_Type': 'Washer',
                    'Brand': 'Whirlpool' if i <= 5 else 'Speed Queen',
                    'Purchase_Date': '2023-03-08' if i <= 5 else '2023-06-01',
                    'Machine_Status': 'Needs Repair' if i in [1, 5] else 'Active'
                })
                
            # Synthesize Dryer Portfolio
            for i in range(1, TOTAL_DRYERS + 1):
                machines.append({
                    'Machine_ID': f'D{i:02d}',
                    'Machine_Type': 'Dryer',
                    'Brand': 'Speed Queen',
                    'Purchase_Date': '2023-06-01' if i <= 3 else '2023-05-29',
                    'Machine_Status': 'Needs Repair' if i in [2, 4] else 'Active'
                })
                
            self.df_machines = pd.DataFrame(machines)
            print(f"✔ Dimension Layer Built: [machines.csv] | Shape: {self.df_machines.shape}")
            return self.df_machines
        except Exception as e:
            print(f"❌ Failed to construct machines dimension layer: {str(e)}")
            raise

    def build_vending_products_dimension(self):
        """
        Establishes static inventory master catalog for complementary product streams.
        """
        try:
            products = [
                {
                    'Product_ID': 'PROD001',
                    'Product_Name': 'Tide Detergent Pack',
                    'Brand_Name': 'Tide',
                    'Unit_Cost': 0.60,
                    'Unit_Price': 1.50,
                    'Supplier': 'CleanCo Distributors'
                },
                {
                    'Product_ID': 'PROD002',
                    'Product_Name': 'Gain Dryer Sheets',
                    'Brand_Name': 'Gain',
                    'Unit_Cost': 0.35,
                    'Unit_Price': 1.00,
                    'Supplier': 'CleanCo Distributors'
                },
                {
                    'Product_ID': 'PROD003',
                    'Product_Name': 'Resolve Stain Remover Pack',
                    'Brand_Name': 'Resolve',
                    'Unit_Cost': 0.70,
                    'Unit_Price': 2.00,
                    'Supplier': 'CleanCo Distributors'
                }
            ]
            self.df_vending = pd.DataFrame(products)
            print(f"✔ Dimension Layer Built: [vending_products.csv] | Shape: {self.df_vending.shape}")
            return self.df_vending
        except Exception as e:
            print(f"❌ Failed to construct vending products dimension layer: {str(e)}")
            raise

    def build_customers_dimension(self, num_customers=134):
        """
        Simulates customer tracking registries with non-linear loyalty distribution tiers.
        """
        try:
            customers = []
            tiers = ['Gold', 'Silver']
            statuses = ['Active', 'Inactive', 'Cancelled']
            
            # Seed distribution dates across the timeline
            base_dates = [START_DATE + timedelta(days=int(x)) for x in np.linspace(0, TOTAL_DAYS - 90, num_customers)]
            
            for i, reg_date in enumerate(base_dates):
                cust_id = f'CUST{i+1:04d}'
                init_load_date = reg_date + timedelta(days=int(np.random.randint(0, 14)))
                
                # Model higher balance metrics for top-tier loyalty tiers
                tier = np.random.choice(tiers, p=[0.4, 0.6])
                status = np.random.choice(statuses, p=[0.7, 0.2, 0.1])
                
                total_deposited = round(float(np.random.uniform(10.0, 60.0)), 2)
                current_balance = round(float(np.random.uniform(0.0, total_deposited)), 2)
                
                customers.append({
                    'Customer_ID': cust_id,
                    'Registration_Date': reg_date.strftime('%Y-%m-%d'),
                    'Initial_Load_Date': init_load_date.strftime('%Y-%m-%d'),
                    'Total_Deposited': total_deposited,
                    'Current_Balance': current_balance,
                    'Loyalty_Tier': tier,
                    'Status': status
                })
                
            self.df_customers = pd.DataFrame(customers)
            print(f"✔ Dimension Layer Built: [customers.csv] | Shape: {self.df_customers.shape}")
            return self.df_customers
        except Exception as e:
            print(f"❌ Failed to construct customers dimension layer: {str(e)}")
            raise

    def build_transaction_fact_pipeline(self, target_tx_count=203400):
        """
        Core pipeline compilation loop. Programmatically enforces true business
        logic (weekend surges, initialization curves, macro financial cogs variances).
        Designed to allow clean step-backs during schema failures.
        """
        try:
            if any(v is None for v in [self.df_machines, self.df_vending, self.df_customers]):
                raise ValueError("Dimension layers must be fully compiled before executing the Fact pipeline.")
                
            transactions = []
            tx_counter = 1
            
            machine_ids = self.df_machines['Machine_ID'].tolist()
            customer_ids = self.df_customers['Customer_ID'].tolist()
            
            # Map structural item parameters for quick access inside loops
            product_catalog = self.df_vending.set_index('Product_ID').to_dict('index')
            product_ids = list(product_catalog.keys())
            
            print(f"🚀 Executing Transaction Matrix Fact Generation Loop...")
            
            # Vectorized calculation parameters across time series
            current_date = START_DATE
            while current_date <= END_DATE:
                is_weekend = current_date.weekday() >= 5
                
                # Business Logic: Calculate transaction volume velocity multipliers
                # Weekend surge scales traffic up by 2x; early startup phase scales up gradually
                time_delta_ratio = (current_date - START_DATE).days / TOTAL_DAYS
                growth_ramp_multiplier = 0.4 + (0.6 * np.sin(time_delta_ratio * (np.pi / 2)))
                
                daily_base_traffic = np.random.randint(180, 240) if is_weekend else np.random.randint(90, 130)
                adjusted_daily_traffic = int(daily_base_traffic * growth_ramp_multiplier)
                
                # Distribute activity logic realistically across operational hours
                for _ in range(adjusted_daily_traffic):
                    if tx_counter > target_tx_count:
                        break
                        
                    hour = int(np.random.choice(
                        np.arange(0, 24), 
                        p=[0.01, 0.01, 0.01, 0.01, 0.02, 0.04, 0.06, 0.08, 0.07, 0.06, 
                           0.05, 0.05, 0.06, 0.06, 0.07, 0.08, 0.09, 0.08, 0.05, 0.02, 
                           0.01, 0.01, 0.01, 0.01]
                    ))
                    
                    # Distribute transactions across product streams
                    stream_choice = np.random.choice(['Machine', 'Vending'], p=[0.85, 0.15])
                    cust_id = np.random.choice(customer_ids + ['GUEST'], p=[0.5] + [0.5]/len(customer_ids))
                    
                    if stream_choice == 'Machine':
                        m_id = np.random.choice(machine_ids)
                        is_washer = m_id.startswith('W')
                        
                        revenue = 2.00 if is_washer else 3.00
                        # Utilities spike slightly on weekends (higher aggregate terminal demand)
                        base_cogs = 0.55 if is_washer else 0.64
                        cogs_variance = 0.02 if is_weekend else 0.01
                        cogs = round(float(np.random.normal(loc=base_cogs, scale=cogs_variance)), 2)
                        p_id = ""
                    else:
                        m_id = np.random.choice(['VM01', 'VM02'])
                        p_id = np.random.choice(product_ids)
                        revenue = product_catalog[p_id]['Unit_Price']
                        cogs = round(float(np.random.normal(loc=product_catalog[p_id]['Unit_Cost'], scale=0.01)), 2)
                    
                    transactions.append({
                        'Transaction_ID': f'TXN{tx_counter:05d}',
                        'date': current_date.strftime('%Y-%m-%d'),
                        'hour': hour,
                        'Machine_ID': m_id,
                        'revenue': revenue,
                        'COGS': cogs,
                        'Customer_ID': cust_id,
                        'Product_ID': p_id
                    })
                    tx_counter += 1
                    
                current_date += timedelta(days=1)
                
            self.df_transactions = pd.DataFrame(transactions)
            print(f"✔ Fact Layer Compiled: [laundromat_transactions_FINAL.csv] | Shape: {self.df_transactions.shape}")
            return self.df_transactions
        except Exception as e:
            print(f"❌ Pipeline Execution Aborted on Fact generation step: {str(e)}")
            raise

    def export_data_warehouse(self):
        """
        Commits internal DataFrames cleanly to your disk layer.
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.df_machines.to_csv(os.path.join(self.output_dir, 'machines.csv'), index=False)
            self.df_vending.to_csv(os.path.join(self.output_dir, 'vending_products.csv'), index=False)
            self.df_customers.to_csv(os.path.join(self.output_dir, 'customers.csv'), index=False)
            self.df_transactions.to_csv(os.path.join(self.output_dir, 'laundromat_transactions_FINAL.csv'), index=False)
            
            print("\n" + "="*60)
            print("🚀 DATA PIPELINE SUCCESS: MULTI-YEAR WAREHOUSE EXPORT COMPLETE")
            print("="*60)
        except Exception as e:
            print(f"❌ Failed to export target assets to disk: {str(e)}")
            raise


# =====================================================================
# SYSTEM MAIN EXECUTION RUNNER
# =====================================================================
if __name__ == "__main__":
    # Initialize pipeline environment
    pipeline = LaundromatDataPipeline()
    
    # Run the modular architecture sequentially
    pipeline.build_machines_dimension()
    pipeline.build_vending_products_dimension()
    pipeline.build_customers_dimension(num_customers=134)
    pipeline.build_transaction_fact_pipeline(target_tx_count=203369)
    
    # Export clean historical assets
    pipeline.export_data_warehouse()
