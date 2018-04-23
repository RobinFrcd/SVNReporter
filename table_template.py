HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<style>
table {{
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
}}

table td, table th {{
    border: 1px solid #ddd;
    padding: 8px;
}}

td a {{ text-align: center; }}

table tr:nth-child(even){{background-color: #f4fff4;}}

table  tr:hover {{background-color: #e1ffdf; border-color: #d3d8d3; }}

table th {{
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}}
</style>
</head>
<body>
 <table>
  <tr>
	<th>Revision</th>
    <th>User</th>
    <th>Date</th>
    <th>Message</th>
	<th>Mod Files</th>
	<th>Remove</th>
  </tr>
  {}
 </table> 
 <script>
	function delete_row(rowId) {{
		document.getElementById(rowId).innerHTML = '';
	}}
	</script>
</body>
</html>
"""