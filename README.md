# Anand Ice Cream - Setup Instructions

## Prerequisites
- Node.js (v14 or higher)
- PostgreSQL (v12 or higher)

## Installation Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Set Up PostgreSQL

**Option A: Local PostgreSQL**
- Install PostgreSQL from https://www.postgresql.org/download/
- During installation, remember your postgres user password
- Start PostgreSQL service:
  ```bash
  # Windows
  # PostgreSQL should start automatically as a service
  
  # Mac
  brew services start postgresql
  
  # Linux
  sudo systemctl start postgresql
  ```

**Option B: PostgreSQL Cloud (ElephantSQL, Supabase, etc.)**
- Create free account at https://www.elephantsql.com/ or https://supabase.com/
- Create a new database instance
- Get connection details
- Update `.env` file with your connection details

### 3. Create Database

**Using psql (PostgreSQL CLI):**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE anand_ice_cream;

# Exit
\q
```

**Using pgAdmin (GUI):**
- Open pgAdmin
- Right-click on "Databases"
- Select "Create" → "Database"
- Name: `anand_ice_cream`
- Click "Save"

### 4. Configure Environment
- Update `.env` file with your PostgreSQL credentials:
  ```env
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=anand_ice_cream
  DB_USER=postgres
  DB_PASSWORD=your_actual_password
  ```

### 5. Start the Server
```bash
npm start
```

The server will automatically create the required tables on first run.

You should see:
```
✅ Connected to PostgreSQL
✅ Database tables initialized
🚀 Server running on http://localhost:3000
```

### 6. Open the Application
- Open `index.html` in your browser
- Or use a local server like Live Server in VS Code

## Database Schema

The `orders` table will be created automatically with the following structure:

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    delivery_address TEXT NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    alternate_phone VARCHAR(20),
    items JSONB NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing the Checkout Flow

1. Add items to cart from the home page
2. Go to cart page
3. Click "Proceed to Checkout"
4. Fill in the form with customer details
5. Click "Checkout" button
6. Order will be saved to PostgreSQL database

## Viewing Orders in Database

**pgAdmin (GUI):**
- Download from https://www.pgadmin.org/download/
- Connect to your PostgreSQL server
- Navigate to: Servers → PostgreSQL → Databases → anand_ice_cream → Schemas → public → Tables → orders
- Right-click on "orders" → "View/Edit Data" → "All Rows"

**psql (CLI):**
```bash
psql -U postgres -d anand_ice_cream

# View all orders
SELECT * FROM orders;

# View orders with formatted JSON
SELECT order_id, full_name, email, items, total_amount, status 
FROM orders 
ORDER BY created_at DESC;

# Exit
\q
```

**Using SQL Query:**
```sql
-- Get all orders
SELECT * FROM orders ORDER BY created_at DESC;

-- Get orders by status
SELECT * FROM orders WHERE status = 'pending';

-- Get customer details with order count
SELECT email, full_name, COUNT(*) as order_count, SUM(total_amount) as total_spent
FROM orders
GROUP BY email, full_name;
```

## API Endpoints

- `GET /api/health` - Check server and database status
- `POST /api/orders` - Create new order
- `GET /api/orders` - Get all orders
- `GET /api/orders/:orderId` - Get specific order

## Troubleshooting

**Server won't start:**
- Check if PostgreSQL is running
- Verify `.env` file has correct database credentials
- Try connecting to PostgreSQL manually: `psql -U postgres`

**Database connection error:**
- Verify PostgreSQL service is running
- Check username and password in `.env`
- Ensure database `anand_ice_cream` exists

**Orders not saving:**
- Check browser console for errors
- Verify server is running on port 3000
- Check server logs for database errors
- Ensure tables were created (check server startup logs)

**CORS errors:**
- Server has CORS enabled by default
- If using different port, update fetch URL in `cart.js`

## PostgreSQL Commands Cheat Sheet

```bash
# Connect to database
psql -U postgres -d anand_ice_cream

# List all databases
\l

# List all tables
\dt

# Describe table structure
\d orders

# View table data
SELECT * FROM orders;

# Count orders
SELECT COUNT(*) FROM orders;

# Delete all orders (careful!)
DELETE FROM orders;

# Drop table (careful!)
DROP TABLE orders;
```