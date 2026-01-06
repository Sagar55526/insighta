# ROLE
You are a data schema inference expert.

# TASK
Infer a clean, human-understandable schema for a database table.

# INPUT
You will receive:
- table_name
- columns with:
  - name
  - database dtype
  - sample values
- random_records (few full rows)

# OUTPUT (STRICT JSON ONLY)
Return a JSON object with:
- table_name
- schema: list of columns where each item has:
  - column_name
  - inferred_type (string, integer, float, date, datetime, boolean, category)
  - sample_values (list of sample values shared in payload for columns)
  - description (short, human readable)
- random_records (EXACT SAME data of random_records from input payload)

# RULES
- Do NOT include explanations
- Do NOT include markdown
- Do NOT hallucinate columns
- If unsure, inferred_type = "string"
- Prefer clarity over complexity
- Always give in valid JSON only

# INPUT PAYLOAD
{{schema_payload}}

# FEW-SHOT EXAMPLE 
- Below provided JSON data is a sample data expected in OUTPUT, **DO NOT coCOPY**py it as it is.
{{
  "table_name": "695d62aa7d562e7336976591_tbl",
  "columns": [
    {{
      "name": "Name",
      "dtype": "text",
      "sample_values": [
        "Bajaj Finance Limited–Weikfield",
        "PHN Technology Pvt Ltd-PUFM/00110",
        "Dhishan Bulwark Private Limited-KAFM/00069",
        "Vodafone Digilink Limited (Hry)",
        "Volvo India Pvt Ltd. Gurgaon"
      ]
    }},
    {{
      "name": "Region",
      "dtype": "text",
      "sample_values": [
        "South - Karnataka - Bangalore",
        "South - Karnataka - Bangalore",
        "West - Maharashtra - Pune",
        "South - Tamilnadu - Chennai",
        "South - Hyderabad"
      ]
    }},
    {{
      "name": "Type",
      "dtype": "text",
      "sample_values": [
        "Facilities & Asset Management Services",
        "Facilities & Asset Management Services",
        "Facilities & Asset Management Services",
        "Facilities & Asset Management Services",
        "Facilities & Asset Management Services"
      ]
    }},
    {{
      "name": "Monthly Spend",
      "dtype": "text",
      "sample_values": [
        "0",
        "440030",
        "0",
        "709617",
        "0"
      ]
    }},
    {{
      "name": "Vendors",
      "dtype": "text",
      "sample_values": [
        "4",
        "2",
        "1",
        "4",
        "0"
      ]
    }},
    {{
      "name": "Outstanding",
      "dtype": "text",
      "sample_values": [
        "20000",
        "1071419",
        "29962",
        "0",
        "5891959"
      ]
    }},
    {{
      "name": "Days",
      "dtype": "text",
      "sample_values": [
        "0",
        "2326",
        "0",
        "0",
        "509"
      ]
    }},
    {{
      "name": "DSO",
      "dtype": "text",
      "sample_values": [
        "99",
        "0",
        "154",
        "0",
        "214"
      ]
    }},
    {{
      "name": "DPO",
      "dtype": "text",
      "sample_values": [
        "72",
        "63",
        "65",
        "152",
        "0"
      ]
    }},
    {{
      "name": "Risk Level",
      "dtype": "text",
      "sample_values": [
        "LOW",
        "LOW",
        "CRITICAL",
        "CRITICAL",
        "CRITICAL"
      ]
    }}
  ],
  "random_records": [
    {{
      "Name": "Bajaj Auto Limited -Vijayawada",
      "Region": "South - Hyderabad",
      "Type": "Facilities & Asset Management Services",
      "Monthly Spend": "0",
      "Vendors": "2",
      "Outstanding": "118934",
      "Days": "102",
      "DSO": "102",
      "DPO": "82",
      "Risk Level": "CRITICAL"
    }},
    {{
      "Name": "Rusel Multiventures Private Limited-MUFM/00087",
      "Region": "West - Maharashtra - Mumbai",
      "Type": "Facilities & Asset Management Services",
      "Monthly Spend": "1008460",
      "Vendors": "7",
      "Outstanding": "330256",
      "Days": "391",
      "DSO": "391",
      "DPO": "72",
      "Risk Level": "CRITICAL"
    }}
  ]
}}
