table_schema = """
            'Table_name': 'new_data', 

            'Table_description': 'This table contains data related to various scenarios in forecasting and reporting models.', 

            'Schema': { 

                '1': { 

                    'Column_name': 'id', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains unique identifiers for the scenarios.' 

                }, 

                '2': { 

                    'Column_name': 'scenario_id', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains unique identifiers for each forecast scenario.' 

                }, 

                '3': { 

                    'Column_name': 'start_year', 

                    'Column_Data_type': 'int', 

                    'Column_description': 'This column contains the start year of the model from which the data is saved.' 

                }, 

                '4': { 

                    'Column_name': 'start_month', 

                    'Column_Data_type': 'int', 

                    'Column_description': 'This column contains the start month of the model from which the data is saved.' 

                }, 

                '5': { 

                    'Column_name': 'start_year_reporting', 

                    'Column_Data_type': 'int', 

                    'Column_description': 'This column contains the start year for reporting purposes.' 

                }, 

                '6': { 

                    'Column_name': 'start_month_reporting', 

                    'Column_Data_type': 'int', 

                    'Column_description': 'This column contains the start month for reporting purposes.' 

                }, 

                '7': { 

                    'Column_name': 'input_output', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column identifies whether the data is a user input or based on model calculations.' 

                }, 

                '8': { 

                    'Column_name': 'for_reporting', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column specifies whether the data is used for reporting.' 

                }, 

                '9': { 

                    'Column_name': 'is_historical', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column identifies whether the data represents historical records.' 

                }, 

                '10': { 

                    'Column_name': 'for_scenario_comparison', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column indicates if the data is used for scenario comparison purposes.' 

                }, 

                '11': { 

                    'Column_name': 'non_business_row_checks', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains checks to identify non-business-related rows.' 

                }, 

                '12': { 

                    'Column_name': 'type_metric_1', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the name of the parameter/metric for which the data is submitted, e.g. patients or doses.' 

                }, 

                '13': { 

                    'Column_name': 'type_metric_2', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the segment name of the patients.' 

                }, 

                '14': { 

                    'Column_name': 'type_metric_3', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the name of the combination if the drug is used with another drug.' 

                }, 

                '15': { 

                    'Column_name': 'type_metric_4', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the brand name of the drug.' 

                }, 

                '16': { 

                    'Column_name': 'type_metric_5', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional segmentation.' 

                }, 

                '17': { 

                    'Column_name': 'type_metric_6', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional segmentation.' 

                }, 

                '18': { 

                    'Column_name': 'type_metric_7', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional segmentation.' 

                }, 

                '19': { 

                    'Column_name': 'type_metric_8', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional segmentation.' 

                }, 

                '20': { 

                    'Column_name': 'type_metric_9', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional segmentation.' 

                }, 

                '21': { 

                    'Column_name': 'type_metric_10', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional segmentation.' 

                }, 

                '22': { 

                    'Column_name': 'concatenated', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains a concatenated key used for mapping and linking data.' 

                }, 

                '23': { 

                    'Column_name': 'extra_1', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '24': { 

                    'Column_name': 'extra_2', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '25': { 

                    'Column_name': 'extra_3', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '26': { 

                    'Column_name': 'extra_4', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '27': { 

                    'Column_name': 'extra_5', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '28': { 

                    'Column_name': 'extra_6', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '29': { 

                    'Column_name': 'extra_7', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '30': { 

                    'Column_name': 'extra_8', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '31': { 

                    'Column_name': 'extra_9', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '32': { 

                    'Column_name': 'extra_10', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column is reserved for additional metadata.' 

                }, 

                '33': { 

                    'Column_name': 'notes_comments', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains any notes or comments regarding the scenario data.' 

                }, 

                '34': { 

                    'Column_name': 'year_value', 

                    'Column_Data_type': 'int', 

                    'Column_description': 'This column contains the year value for which the data is submitted.' 

                }, 

                '35': { 

                    'Column_name': 'data_value', 

                    'Column_Data_type': 'double', 

                    'Column_description': 'This column contains the data value or measure.' 

                }, 

                '36': { 

                    'Column_name': 'date_value', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the month or date for which the data is submitted.' 

                }, 

                '37': { 

                    'Column_name': 'forecast_cycle_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the name of the forecast cycle, such as operational cycle or operational plan.' 

                }, 

                '38': { 

                    'Column_name': 'forecast_year', 

                    'Column_Data_type': 'int', 

                    'Column_description': 'This column contains the forecast year for which the data is submitted.' 

                }, 

                '39': { 

                    'Column_name': 'therapy_area', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the therapy area related to the forecast data.' 

                }, 

                '40': { 

                    'Column_name': 'brand_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the name of the brand or franchise.' 

                }, 

                '41': { 

                    'Column_name': 'indication_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the name of the indication associated with the forecast data.' 

                }, 

                '42': { 

                    'Column_name': 'country_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the country name associated with the forecast data.' 

                }, 

                '43': { 

                    'Column_name': 'region_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the region or area associated with the forecast data.' 

                }, 

                '44': { 

                    'Column_name': 'model_id', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains unique identifiers for models related to the forecast data.' 

                }, 

                '45': { 

                    'Column_name': 'scenario_type_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the type of scenario, such as base scenario, upside scenario, or downside scenario.' 

                }, 

                '46': { 

                    'Column_name': 'scenario_name', 

                    'Column_Data_type': 'varchar', 

                    'Column_description': 'This column contains the name of the scenario as submitted by the user.' 

                }, 

                '47': { 

                    'Column_name': 'description', 

                    'Column_data_type’:’varchar’, 

                    ‘column_description’: ‘this column contains the description of the scenario as submitted by the user’ 

                }, 

                '48':{ 

                    ‘Column_name’: ‘submitted_by’, 

                ‘Column_data_type’: ‘varchar’, 

                ‘Column_description’: ‘User who have submitted the scenario’, 

            }, 

                '49':{ 

                ‘Column_name’: ‘submitted_on’, 

                ‘Column_data_type’: ‘varchar’, 

                ‘Column_description’: ‘ET time when the scenario got last saved/updated’, 

                } 

                } 
            """
