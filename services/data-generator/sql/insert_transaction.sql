INSERT INTO transactions (
                step, transaction_id, source_user_id, dest_user_id, amount, payment_method, transaction_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)