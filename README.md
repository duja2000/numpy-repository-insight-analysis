\----------------------Repository Insight Analysis: NumPy-----------------



This project conducts a structured empirical analysis of the GitHub repository `numpy/numpy`.



\-------------------------- Research Question------------------------------



RQ1 — How does development activity evolve over time?



The analysis investigates monthly commit counts and code churn across the lifetime of the NumPy repository.



\------------------------Repository Studied-------------------------



\- Repository: https://github.com/numpy/numpy

\- Analysis period: December 2001 to May 2026

\- Commits analyzed: 31,075 non-merge commits



\----------------------------Tools Used------------------------------------



\- Git

\- Python

\- pandas

\- matplotlib



\------------------------ Project Structure------------------------



numpy-repository-insight-analysis/

\- analysis.py

\- summary\_stats.py

\- README.md

\- requirements.txt

\- data/

&#x20; - monthly\_activity.csv

&#x20; - summary\_stats.txt

\- plots/

&#x20; - monthly\_commits\_churn\_timeseries.png

&#x20; - churn\_distribution.png

&#x20; - activity\_heatmap.png

\- report/

&#x20; - reflection\_report.pdf

&#x20; - ai\_usage\_transcript.pdf



\------------------------------- Reproducibility Instructions---------------------------------------



1\. Clone the NumPy repository:



&#x20;   git clone https://github.com/numpy/numpy.git data/numpy



2\. Extract Git log data:



&#x20;   git -C data/numpy log --no-merges --date=short --numstat --pretty=format:"@@@%H|%ad|%an|%ae" > data/raw\_git\_log.txt



3\. Install dependencies:



&#x20;   pip install -r requirements.txt



4\. Run the analysis:



&#x20;   python analysis.py



5\. Generate summary statistics:



&#x20;   python summary\_stats.py



The cleaned monthly dataset will be saved in the `data/` folder, and the generated plots will be saved in the `plots/` folder.



\------------------------------------- Data Cleaning Notes--------------------------------------------------



Merge commits were excluded using `--no-merges` to reduce duplicated integration activity. Binary file changes were excluded from churn calculations because Git reports them with dash symbols instead of numeric line additions and deletions.



Code churn was calculated as:



total churn = lines added + lines removed



\------------------------------------ AI Usage Transparency---------------------------------------------------------



AI assistance was used to support assignment understanding, project planning, coding guidance, debugging, and report writing clarity. The empirical results were generated from the locally cloned NumPy repository using the provided Git and Python scripts. A PDF copy of the AI assistance session is included in the `report/` folder.

