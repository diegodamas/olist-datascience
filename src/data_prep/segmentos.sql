--Table Analytics - Recency, frequency, monetary value (RFM) [Recência, Frequencia e Valor (RFV)]
USE olist;
SELECT T1.*,
        CASE WHEN pct_receita <= 0.5 AND pct_freq <= 0.5 THEN 'LOW VALUE AND LOW FREQUENCY'
            WHEN pct_receita > 0.5 AND pct_freq <= 0.5 THEN 'HIGH VALUE'
            WHEN pct_receita <= 0.5 AND pct_freq > 0.5 THEN 'HIGH FREQUENCY'
            WHEN pct_receita < 0.9 OR pct_freq < 0.9 THEN 'PROFITABLE'
            ELSE 'SUPER PROFITABLE'
        END AS SEGMENTO_VALOR_FREQ,

        CASE WHEN qtde_dias_base <= 60 THEN 'START'
                WHEN qtde_dias_ult_venda >= 300 THEN 'RETENTION'
                ELSE 'ACTIVE'
        END AS SEGMENTO_VIDA,
        '{date_end}' AS DT_SGMT

FROM (

    SELECT T1.*,
        percent_rank() over (order by receita_total asc) as pct_receita,
        percent_rank() over (order by qtde_pedidos asc) as pct_freq

    FROM (

        SELECT T2.seller_id,
                SUM( T2.price ) AS receita_total,
                COUNT(DISTINCT T1.order_id ) AS qtde_pedidos,
                COUNT( T2.product_id ) AS qtde_produtos,
                COUNT(DISTINCT T2.product_id ) AS qtde_produtos,
                MIN( CAST(julianday('{date_end}') - julianday(T1.order_approved_at) AS INT) ) AS qtde_dias_ult_venda,
                MAX( CAST(julianday( '{date_end}' ) - julianday( dt_inicio ) AS INT ) ) AS qtde_dias_base

        FROM tb_orders AS T1

        LEFT JOIN tb_order_items as T2
        ON T1.order_id = T2.order_id

        LEFT JOIN (
            SELECT T2.seller_id,
                MIN( DATE( T1.order_approved_at ) ) AS dt_inicio
            FROM tb_orders AS T1
            LEFT JOIN tb_order_items AS T2
            ON T1.order_id = T2.order_id
            GROUP BY T2.seller_id
        ) AS T3
        ON T2.seller_id = T3.seller_id

        WHERE T1.order_approved_at BETWEEN '{date_init}' AND '{date_end}'

        GROUP BY T2.seller_id

    ) AS T1

) AS T1 WHERE seller_id IS NOT NULL;