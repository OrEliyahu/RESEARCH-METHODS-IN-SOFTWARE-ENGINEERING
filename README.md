# RESEARCH-METHODS-IN-SOFTWARE-ENGINEERING
interface for compare and analyze surveys results


Requirements:
Python3
Flask
pandas

To run the interface run python main.py and then navigate to http://127.0.0.1:5000/ in your browser.


Full fllow after update tables:
1. Change values in talbes and click save. Saving updates relevant table in "tables"
2. Click compare to update relevant question in "summaries"
	* If you change multiple tables and don't want to click compare for each one of them than run "update_summaries.py" ("main.py" must run in background)
3. Run "results_analysis_scripts/concepts_diversity.py" to update "results_analysis_scripts/distribution"
4. Run "questionnaire/fix_results.py" to update jedges results and than run "questionnaire/extract_results.py"