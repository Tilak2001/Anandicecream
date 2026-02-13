-- Add payment columns to existing orders table
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS payment_screenshot TEXT,
ADD COLUMN IF NOT EXISTS payment_status VARCHAR(50) DEFAULT 'pending';

-- Create index for payment_status
CREATE INDEX IF NOT EXISTS idx_payment_status ON orders(payment_status);
