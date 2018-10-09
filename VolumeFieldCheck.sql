SELECT
CONCAT('i',item_view.record_num, 'a', '          ', field_content) 
--adds i prefix to the item record number and the "a" as a placeholder for the check digit, so the number can be easily copied and pasted into Sierra, also includes the text of the volume field

FROM sierra_view.varfield_view
JOIN sierra_view.item_view ON varfield_view.record_num = item_view.record_num

WHERE 
record_creation_date_gmt > TIMESTAMP 'yesterday' AND 
varfield_view.record_type_code =  'i' AND 
varfield_type_code = 'v'
-- This limits results to any item records created since midnight of the previous day, that contain something in the volume field

ORDER BY field_content
--sorts results alphabetically by the text included in the volume field