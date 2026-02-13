const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'anand_ice_cream',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD
});

async function migrateDatabase() {
    try {
        console.log('🔄 Running database migration...');

        // Add payment columns
        await pool.query(`
            ALTER TABLE orders 
            ADD COLUMN IF NOT EXISTS payment_screenshot TEXT,
            ADD COLUMN IF NOT EXISTS payment_status VARCHAR(50) DEFAULT 'pending';
        `);

        console.log('✅ Added payment_screenshot and payment_status columns');

        // Create index
        await pool.query(`
            CREATE INDEX IF NOT EXISTS idx_payment_status ON orders(payment_status);
        `);

        console.log('✅ Created payment_status index');
        console.log('✅ Migration completed successfully!');

    } catch (error) {
        console.error('❌ Migration failed:', error);
    } finally {
        await pool.end();
    }
}

migrateDatabase();
