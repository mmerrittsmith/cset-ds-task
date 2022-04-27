# answer_qs.py
from pathlib import Path
import jsonlines
import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple

def fr_in_title_or_abstract(arxiv_line: dict) -> bool:
	"""
	fr_in_title_or_abstract:
	Takes in a single line of the arxiv.jsonl file and returns
	True if any synonymous phrase of "facial recognition" appears
	in the title or abstract, and false otherwise
	"""
	fr_synonyms = ["biometric identification", "face recognition", 
				   "biometric authentication", "facial recognition",
				   "biometric recognition", "face detection"]
	title = arxiv_line['title'].lower()
	abstract = arxiv_line['abstract'].lower()
	return any([re.search(synonym, title) or re.search(synonym, abstract) for synonym in fr_synonyms])


def fr_in_topic(arxiv_line: dict) -> bool:
	"""
	fr_in_topic_list: 
	Takes in a single line of the arxiv.jsonl file and returns
	True if the line is in the computer vision category and false otherwise
	"""
	return "cs.CV" in arxiv_line["categories"]


def compare_titles_abstracts_and_topics(fr_in_titles_abstracts_list: list,
										fr_in_topic_list: list
										) -> None:
	"""
	compare_titles_abstracts_and_topics:
	Takes in two lists of dicts, first the list of lines from arxiv.jsonl
	that refer to papers that have something about facial recognition in the
	title or abstract and second the lines that have computer vision as one of
	the topics. Calculates some statistics based on set operations between the
	two lists and prints those. Returns nothing.
	"""
	titles_abstracts_ids = [line['id'] for line in fr_in_titles_abstracts_list]
	topics_ids = [line['id'] for line in fr_in_topic_list]
	print(f"""
  		  There are {len(titles_abstracts_ids)} papers with something about facial recognition 
		  in their titles and abstracts, and {len(topics_ids)} papers with facial recognition
		  as their category. There are {len(set(titles_abstracts_ids).intersection(set(topics_ids)))} shared papers between these, and therefore 
		  {len(set(titles_abstracts_ids).union(set(topics_ids)))} in total. 

		  {round((1-(len(set(titles_abstracts_ids).difference(topics_ids))/(len(titles_abstracts_ids))))*100, 2)}% of the papers with something about facial recognition
		  in their titles or abstracts are in the the computer vision category. Conversely, {round((1-(len(set(topics_ids).difference(titles_abstracts_ids))/(len(topics_ids))))*100, 2)}%
		  of the papers in the computer vision category have something about facial recognition in the title or abstract.
		  """)

def generate_plots(fr_in_titles_abstracts_list: list,
				   fr_in_topic_list: list,
				   all_papers: list
				   ) -> None:
	"""
	generate_plots:
	Takes in three lists, each of which are composed of dicts, each dict being a 
	row from the jsonl file. all_papers has every single row from the jsonl file.
	This function generates three plots: One that shows the number of facial recognition
	papers started by year, one that shows the % change for # of facial recognition papers 
	from the previous year, and one that shows the % of total paper count for facial 
	recognition papers. 
	Returns None.
	"""
	titles_abstracts_ids = [line['id'] for line in fr_in_titles_abstracts_list]
	topics_ids = [line['id'] for line in fr_in_topic_list]
	fr_lines = list(set(titles_abstracts_ids).intersection(set(topics_ids)))
	lines_in_common = [line for line in fr_in_titles_abstracts_list+fr_in_topic_list if line['id'] in fr_lines]
	fr_df = pd.DataFrame(lines_in_common)
	fr_df = fr_df.drop_duplicates(subset='id')
	fr_by_year = create_df_grouped_by_year(fr_df)

	# Adjusting for the fact that we don't have all the data in 2019
	# We only have papers up to the end of August
	average_papers_per_month_2019 = fr_by_year.loc[2019]['Number of Papers Started']/8
	fr_by_year.loc[2019]['Number of Papers Started'] =  round(fr_by_year.loc[2019]['Number of Papers Started']+4*average_papers_per_month_2019,0)

	sns.set(rc={"figure.figsize":(10, 10)})
	sns.set_theme(style="dark")
	sns.barplot(data=fr_by_year, x='Year', y='Number of Papers Started').set_title("Number of Facial Recogntion Papers Started By Year")
	sns.despine()
	plt.savefig('papers_started_by_year.png')
	plt.clf()

	change_over_time_papers_started = fr_by_year.pct_change()
	change_over_time_papers_started['Year'] = fr_by_year['Year'][1:]
	ax = sns.barplot(data=change_over_time_papers_started, x='Year', y='Number of Papers Started')
	ax.set(ylabel='% Change from Previous Year for Facial Recognition Papers Started',
		   title='% Change Year over Year for Facial Recognition')
	plt.savefig('papers_started_pct_change.png')
	plt.clf()


	all_papers = pd.DataFrame(all_papers)
	all_papers_by_year = create_df_grouped_by_year(all_papers)
	all_papers_by_year.to_csv('all_papers_by_year.csv')
	average_papers_per_month_2019 = all_papers_by_year.loc[2019]['Number of Papers Started']/9
	all_papers_by_year.loc[2019]['Number of Papers Started'] =  round(all_papers_by_year.loc[2019]['Number of Papers Started']+4*average_papers_per_month_2019,0)
	all_papers_by_year = all_papers_by_year.merge(fr_by_year, how='left', left_index=True, right_index=True)
	all_papers_by_year = all_papers_by_year.drop(columns='Year_y')
	all_papers_by_year = all_papers_by_year.rename(columns={'Year_x': "Year"})
	all_papers_by_year = all_papers_by_year.rename(columns={'Number of Papers Started_x': "Number of Papers Started", "Number of Papers Started_y": "Number of Facial Recogntion Papers Started"})
	all_papers_by_year['Facial recognition papers as pct. of all papers'] = (all_papers_by_year['Number of Facial Recogntion Papers Started'] / all_papers_by_year['Number of Papers Started'])*100
	all_papers_by_year = all_papers_by_year[all_papers_by_year['Year'] > 2003]
	sns.barplot(data=all_papers_by_year, x='Year', y='Facial recognition papers as pct. of all papers').set_title("Number of C.V. Papers Started as % of All Papers Started")
	plt.savefig('fr_papers_as_pct_of_total_by_year.png')
	plt.clf()


def create_df_grouped_by_year(df: pd.DataFrame) -> pd.DataFrame:
	"""
	create_df_grouped_by_year:
	Groups the dataframe by year and gets the row count by year.
	Returns the grouped dataframe.
	"""
	df['created'] = pd.to_datetime(df['created'])
	df['Year'] = df['created'].dt.year
	df['Number of Papers Started'] = 1
	df_by_year = df.groupby('Year').count()
	df_by_year['Year'] = df_by_year.index.tolist()
	return df_by_year	

def read_data() -> Tuple[list, list, list]:
	"""
	read_data()
	Reads in lines from arxiv.jsonl, creating three separate 
	lists of dicts from the rows of the file based on the topic of
	the paper, the text of the title or abstract, or in the case of 
	all_lines regardless of those attributes. 
	Returns a tuple of all three lists
	"""
	arxiv_path = Path.cwd() / 'arxiv.jsonl'
	fr_in_titles_abstracts_list = []
	fr_in_topic_list = []
	all_lines = []
	with jsonlines.open(arxiv_path, 'r') as f:
		for line_num, line in enumerate(f.iter()):
			if fr_in_title_or_abstract(line):
				fr_in_titles_abstracts_list.append(line)
			if fr_in_topic(line):
				fr_in_topic_list.append(line)
			all_lines.append(line)
	return fr_in_titles_abstracts_list, fr_in_topic_list, all_lines


def main():
	"""
	main():
	Controls top-level functionality for answer_qs.py
	"""
	fr_in_titles_abstracts_list, fr_in_topic_list, all_lines = read_data()
	compare_titles_abstracts_and_topics(fr_in_titles_abstracts_list, fr_in_topic_list)
	generate_plots(fr_in_titles_abstracts_list, fr_in_topic_list, all_lines)


if __name__ == '__main__':
	main()