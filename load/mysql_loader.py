from database import get_connection
from utils.logger import logger
from datetime import datetime


# =========================================================
# TOOL METADATA
# =========================================================

tool_metadata = {

    "ChatGPT": (
        "OpenAI",
        "chatgpt.com"
    ),

    "Gemini": (
        "Google",
        "gemini.google.com"
    ),

    "Claude｜Anthropic": (
        "Anthropic",
        "claude.ai"
    ),

    "DeepSeek": (
        "DeepSeek",
        "deepseek.com"
    ),

    "Grok": (
        "xAI",
        "grok.com"
    ),

    "豆包｜抖音": (
        "ByteDance",
        "doubao.com"
    ),

    "copilot｜微软": (
        "Microsoft",
        "copilot.microsoft.com"
    ),

    "AI 搜索｜百度": (
        "Baidu",
        "yiyan.baidu.com"
    ),

    "千问 qianwen.com｜阿里": (
        "Alibaba",
        "qianwen.com"
    ),

    "Kimi｜月之暗面": (
        "Moonshot AI",
        "kimi.com"
    ),

    "Qwen.ai｜阿里": (
        "Alibaba",
        "qwen.ai"
    ),

    "meta.ai": (
        "Meta",
        "meta.ai"
    ),

    "Adot｜韩语": (
        "SK Telecom",
        "adot.ai"
    ),

    "Venice": (
        "Venice AI",
        "venice.ai"
    ),

    "腾讯元宝": (
        "Tencent",
        "yuanbao.tencent.com"
    ),

    "Z.ai": (
        "Zhipu AI",
        "z.ai"
    ),

    "DeepAI": (
        "DeepAI",
        "deepai.org"
    ),

    "Mistral": (
        "Mistral AI",
        "mistral.ai"
    ),

    "Poe": (
        "Quora",
        "poe.com"
    ),

    "智谱清言": (
        "Zhipu AI",
        "chatglm.cn"
    )
}


# =========================================================
# LOAD CATEGORY
# =========================================================

def load_category():

    connection = get_connection()

    if connection is None:
        logger.error("Database connection failed")
        return

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO Dim_Category
    (Category_Name)
    VALUES (%s)
    """

    cursor.execute(query, ("AI Chatbot",))

    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Category loaded successfully")


# =========================================================
# LOAD SUBSCRIPTION
# =========================================================

def load_subscription():

    connection = get_connection()

    if connection is None:
        logger.error("Database connection failed")
        return

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO Dim_Subscription
    (Pricing_Type, Monthly_Price, Yearly_Price)
    VALUES (%s, %s, %s)
    """

    values = (
        "Unknown",
        None,
        None
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Subscription loaded successfully")


# =========================================================
# LOAD TOOLS
# =========================================================

def load_tools(data):

    connection = get_connection()

    if connection is None:
        logger.error("Database connection failed")
        return

    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # GET CATEGORY ID
        # -------------------------------------------------

        category_query = """
        SELECT Category_ID
        FROM Dim_Category
        WHERE Category_Name = %s
        """

        cursor.execute(
            category_query,
            ("AI Chatbot",)
        )

        category_result = cursor.fetchone()

        if category_result is None:
            logger.error("AI Chatbot category not found")
            return

        category_id = category_result[0]

        # -------------------------------------------------
        # GET SUBSCRIPTION ID
        # -------------------------------------------------

        subscription_query = """
        SELECT Subscription_ID
        FROM Dim_Subscription
        WHERE Pricing_Type = %s
        """

        cursor.execute(
            subscription_query,
            ("Unknown",)
        )

        subscription_result = cursor.fetchone()

        if subscription_result is None:
            logger.error("Unknown subscription type not found")
            return

        subscription_id = subscription_result[0]

        # -------------------------------------------------
        # INSERT OR UPDATE TOOLS
        # -------------------------------------------------

        insert_query = """
        INSERT INTO Dim_Tool
        (
            Tool_Name,
            Company_Name,
            Website_Name,
            Category_ID,
            Subscription_ID
        )
        VALUES (%s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE

            Company_Name = VALUES(Company_Name),
            Website_Name = VALUES(Website_Name),
            Category_ID = VALUES(Category_ID),
            Subscription_ID = VALUES(Subscription_ID)
        """

        for _, row in data.iterrows():

            tool_name = row["Tool"]

            if tool_name not in tool_metadata:

                logger.warning(
                    f"Metadata not found for: {tool_name}"
                )

                continue

            company_name, website_name = tool_metadata[tool_name]

            values = (
                tool_name,
                company_name,
                website_name,
                category_id,
                subscription_id
            )

            cursor.execute(
                insert_query,
                values
            )

        connection.commit()

        logger.info("Tools loaded successfully")

    except Exception as e:

        connection.rollback()

        logger.error(
            f"Error loading tools: {e}"
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# LOAD TOOL STATISTICS
# =========================================================

def load_statistics(data,data_month):

    connection = get_connection()

    if connection is None:
        logger.error("Database connection failed")
        return

    cursor = connection.cursor()



    for _, row in data.iterrows():

        tool_name = row["Tool"]
        monthly_visits = row["Monthly_Visits"]

        # Find Tool_ID
        find_tool_query = """
        SELECT Tool_ID
        FROM Dim_Tool
        WHERE Tool_Name = %s
        """

        cursor.execute(find_tool_query, (tool_name,))

        result = cursor.fetchone()

        if result is None:
            logger.warning(f"Tool not found: {tool_name}")
            continue

        tool_id = result[0]

        # Check whether this tool already has this month's data
        check_query = """
        SELECT Statistic_ID
        FROM Fact_Tool_Statistics
        WHERE Tool_ID = %s
        AND Data_Month = %s
        """

        cursor.execute(check_query, (tool_id, data_month))

        existing_record = cursor.fetchone()

        if existing_record:

            # UPDATE existing record
            update_query = """
            UPDATE Fact_Tool_Statistics
            SET Monthly_Visits = %s,
                Last_Update = NOW()
            WHERE Statistic_ID = %s
            """

            cursor.execute(
                update_query,
                (monthly_visits, existing_record[0])
            )

        else:

            # INSERT new monthly record
            insert_query = """
            INSERT INTO Fact_Tool_Statistics
            (Tool_ID, Monthly_Visits, Last_Update, Data_Month)
            VALUES (%s, %s, NOW(), %s)
            """

            cursor.execute(
                insert_query,
                (tool_id, monthly_visits, data_month)
            )

    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Tool statistics loaded successfully")