"""第 6 课 Text2SQL MVP 的 Prompt 构造模块。"""


SCHEMA = """
表：dim_customers（客户维度表）
- customer_id INT 主键
- customer_name VARCHAR(100) 客户名称
- customer_type VARCHAR(50) 客户类型
- industry VARCHAR(50) 客户行业
- country VARCHAR(50) 国家
- region VARCHAR(50) 大区

表：dim_products（产品维度表）
- product_id INT 主键
- product_name VARCHAR(100) 产品名称
- product_line VARCHAR(50) 产品线
- category VARCHAR(50) 产品分类
- tech_route VARCHAR(50) 技术路线
- standard_cost DECIMAL(10,2) 标准成本
- material_cost DECIMAL(10,2) 材料成本
- labor_cost DECIMAL(10,2) 人工成本

表：sales_orders（销售订单表）
- order_id BIGINT 主键
- order_no VARCHAR(50) 订单编号
- customer_id INT 外键 -> dim_customers.customer_id
- product_id INT 外键 -> dim_products.product_id
- region VARCHAR(50) 销售区域
- order_date DATE 订单日期
- order_status VARCHAR(20) 订单状态：completed/cancelled/pending
- quantity DECIMAL(10,2) 数量
- unit_price DECIMAL(10,2) 单价
- discount_amount DECIMAL(12,2) 折扣金额
- gross_amount DECIMAL(12,2) 含税总额
- net_amount DECIMAL(12,2) 不含税收入
- currency VARCHAR(10) 币种

表：exchange_rates（汇率表）
- rate_date DATE 日期
- currency VARCHAR(10) 币种
- rate_to_cny DECIMAL(10,4) 兑人民币汇率

表：finance_expenses（费用表）
- expense_id BIGINT 主键
- expense_date DATE 费用日期
- department VARCHAR(50) 部门
- rd_expense DECIMAL(12,2) 研发费用
- selling_expense DECIMAL(12,2) 销售费用
- admin_expense DECIMAL(12,2) 管理费用
- finance_expense DECIMAL(12,2) 财务费用
- marketing_expense DECIMAL(12,2) 市场费用
- logistics_expense DECIMAL(12,2) 物流费用
- warranty_expense DECIMAL(12,2) 质保费用
""".strip()


FEW_SHOT_EXAMPLES = """
示例 1（Example 1）：
问题：查询已完成订单的总数量。
SQL：SELECT COUNT(*) AS order_count FROM sales_orders WHERE order_status = 'completed';

示例 2：
问题：按客户类型统计已完成订单数量。
SQL：SELECT c.customer_type, COUNT(*) AS order_count FROM sales_orders AS o JOIN dim_customers AS c ON o.customer_id = c.customer_id WHERE o.order_status = 'completed' GROUP BY c.customer_type;

示例 3：
问题：查询 2026 年第一季度的总费用。
SQL：SELECT SUM(rd_expense + selling_expense + admin_expense + finance_expense) AS total_expense FROM finance_expenses WHERE expense_date >= '2026-01-01' AND expense_date < '2026-04-01';
""".strip()


SYSTEM_MESSAGE = "你是一名专业的 MySQL SQL 生成助手（SQL generation assistant）。"


def build_prompt(user_question: str, use_few_shot: bool = True) -> tuple[str, str]:
    """构造供 ``LLMClient`` 调用的系统消息与用户消息。"""
    sections = [f"【数据库 Schema】\n{SCHEMA}"]

    if use_few_shot:
        sections.append(f"【示例】\n{FEW_SHOT_EXAMPLES}")

    sections.append(
        f"""【用户问题】
{user_question}

【要求】
1. 只输出一条 SELECT 查询语句（only one SELECT statement），不要解释或 Markdown 代码块。
2. 使用标准 MySQL 语法，且只能使用 Schema 中的表名和字段名。
3. 涉及销售额或收入时，使用 sales_orders.net_amount，并过滤已完成订单。
4. 禁止生成 INSERT、UPDATE、DELETE、DROP、ALTER 或任何其他写操作。"""
    )

    return SYSTEM_MESSAGE, "\n\n".join(sections)
