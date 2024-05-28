import pprint
import asyncio
from data_manage_fce import load_json_data, aggregate_survey_dataset
from graphing import Bargraph, excel_pivot_table, Sunburstgraph

async def main():
    pp = pprint.PrettyPrinter(depth=4)
    data = await load_json_data('fake_data.json')

    for survey in data['surveyPage']:
        processed_data = list(aggregate_survey_dataset(survey))
        pp.pprint(processed_data)
    data = processed_data

    Bargraph(data)
    excel_pivot_table(data)
    Sunburstgraph(data)

asyncio.run(main())