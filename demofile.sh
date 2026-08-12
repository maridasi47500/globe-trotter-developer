
mkdir templates 
python3 scaffold.py clean_code name description
python3 scaffold.py traveler_status status description date
python3 scaffold.py user username email password phone country_id:references
python3 scaffold.py country name
python3 scaffold.py user_traveler user_id:references traveler_status_id:references
python3 scaffold.py product description user_id:references date
python3 scaffold.py rspectdd name
python3 scaffold.py producthascleancode product_id:references clean_code_id:references
python3 scaffold.py producthasrspectdd product_id:references rspectdd_id:references
