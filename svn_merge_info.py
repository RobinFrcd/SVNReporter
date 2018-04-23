import argparse
import subprocess

from table_template import HTML_TEMPLATE

parser = argparse.ArgumentParser(description='SVN Branches Paths')
parser.add_argument('--trunk', help='TRUNK url (merge into)', required=True)
parser.add_argument('--branch', help='BRANCH url (merge from)', required=True)
parser.add_argument('--skip_starred', help='Exclude revisions marked with a *', action='store_true')
args = parser.parse_args()

SVN_SPLIT = '------------------------------------------------------------------------'
IGNORED_USERS = ['jenkins']

def getMergeInfo(branch, trunk):
	print('Merge Info between: \n BRANCH: {} \n TRUNK: {}'.format(branch, trunk))
	print('Skip starred revisions:', args.skip_starred)
	
	cmd = 'svn mergeinfo --show-revs eligible {} {}'.format(branch, trunk)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	revisions = p.stdout.readlines()
	revisions = [rev.decode().replace('\r\n', '') for rev in revisions]
	
	cleaned_revs = list()
	for rev in revisions:
		if '*' not in rev:
			cleaned_revs.append({'id': rev, 'starred': False})
		elif '*' in rev and not args.skip_starred:
			cleaned_revs.append({'id': rev.replace('*', ''), 'starred': True})
			print('Include starred revision: ', rev)
		elif '*' in rev and args.skip_starred:
			print('Skipping: ', rev)
			
	return cleaned_revs

	
def revision_info(rev_id, branch):
	cmd = 'svn log --verbose -r {} {}'.format(rev_id, branch)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	revison_info_list = output.decode()\
		.replace(SVN_SPLIT, '')\
		.split('|')
	detail_message = revison_info_list[3].split('\r\n\r\n')
	mod_files = detail_message[0].split('\r\n')
	try:
		mod_files = [file.strip() for file in mod_files[2:]]
	except IndexError:
		pass

	revison_info = {
		'user': revison_info_list[1].strip(),
		'date': revison_info_list[2][-18:-2].strip(),
		'message': detail_message[1].replace('\r\n', ' ').strip(),
		'mod_files': mod_files
	}
	
	return revison_info
	
def main():	
	revisions = getMergeInfo(args.branch, args.trunk)
	print('{} revisions:'.format(len(revisions)))
	table_content = ""
	for full_rev in revisions:
		rev_id = full_rev['id'][1:]
		rev_info = revision_info(rev_id, args.branch)
		if full_rev['starred']:
			rev_id += '(*)'
		if rev_info['user'] in IGNORED_USERS:
			print("{} is a {}'s commit, skip".format(rev_id, rev_info['user']))
		else:	
			print('Revision: ' + rev_id)
			table_content += "<tr id='{0}'><td>{0}</td><td>{1}</td><td>{2}</td><td>{3} ({1})</td>"\
							.format(rev_id, rev_info['user'], rev_info['date'], rev_info['message'])
			mod_files = ''.join("<li>{}</li>".format(mod_file) for mod_file in rev_info['mod_files'])
			table_content += "<td><ul>{}</ul></td>".format(mod_files)
			table_content += '<td><button onclick="delete_row(\'{}\')">X</button></tr>'.format(rev_id)
		
	html_table = HTML_TEMPLATE.format(table_content)
	with open('merge_info.html', 'w') as f:
		f.write(html_table)
		
if __name__ == "__main__":
	main()
	