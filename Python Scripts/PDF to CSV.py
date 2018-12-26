import tabula

file_name = "mcd_ca"

# convert PDF into CSV
tabula.convert_into(file_name + ".pdf", file_name + ".csv", output_format="csv", pages = 'all', multiple_tables=True)
