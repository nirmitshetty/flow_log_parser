# Flow log parser
This program parses a flow log file, matching each row with a tag based on a lookup table, and generates an output file containing:
- tag counts
- port/protocol combination counts

## Files
1. Flow log file: Sample files are present in `test` directory.
2. Lookup table file: Default lookup table is `lookup_table.txt` in input directory. Can be changed in `config.py`. 
3. Output file: File is generated in `output` directory and format is `output_<flow log filepath>.txt`.

## Assumptions
1. Lookup table
   - Space delimited text file
   - Only consider rows with at least 3 fields
   - All fields are valid
   - One port,protocol combination maps to one tag
   - One tag can map to one or more (port,protocol) combinations
   - Unmapped (port,protocol) combinations are tagged as 'Untagged'
2. Protocol number mapping
   - Pre-defined hashmap with protocol number to names mapped. Defined in `config.py`
3. Flow logs
   - Space delimited text file
   - Only consider rows with at least `14` fields
   - Only consider rows with version `2`
   - Only consider rows with action `ACCEPT`
   - Only consider rows with log-status `OK` 
   - Only consider rows with protocol numbers that are pre-defined in the mapping
   - Remaining fields are valid
   - Matching is case-insensitive
4. Output
   - Text file
   - No strict ordering of rows

## Example Usage
**Python Version**: 3.9 or higher.
Use the following Python command to run the program:
```
python flow_log_parser.py <flow_log_filepath>
e.g.: python flow_log_parser.py test/sample_1.txt 
```

## Testing
Apart from the sample input file, the following scenarios were tested:
- rows with insufficient fields
- rows with invalid version
- rows with invalid action
- rows with invalid log-status
- empty logs
- rows with unmapped protocol numbers
