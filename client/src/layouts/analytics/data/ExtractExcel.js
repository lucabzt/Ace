const xlsx = require('xlsx');
const fs = require('fs');
const path = require('path');

// Function to extract data from Excel and inject it into the JavaScript file
function updateLineChartDataDashboard(excelFilePath, jsFilePath, optionsFilePath) {
  // Load the workbook
  const workbook = xlsx.readFile(excelFilePath);

  // Access the sheet named "Overview"
  const sheetName = 'Overview';
  const worksheet = workbook.Sheets[sheetName];

  if (!worksheet) {
    console.error(`Sheet "${sheetName}" not found in the workbook.`);
    return;
  }

  // Convert sheet data to JSON
  const jsonData = xlsx.utils.sheet_to_json(worksheet, { header: 1 });

  // Locate all occurrences of "SPIELER"
  const movingSumStartRows = [];
  jsonData.forEach((row, index) => {
    if (row[0] === 'SPIELER') {
      movingSumStartRows.push(index);
    }
  });

  if (movingSumStartRows.length < 2) {
    console.error(`The second "SPIELER" table not found in the sheet.`);
    return;
  }

  // Use the second "SPIELER" table
  const movingSumStartRow = movingSumStartRows[1];

  // Extract the header row and data rows
  const headers = jsonData[movingSumStartRow];
  const dataRows = jsonData.slice(movingSumStartRow + 1).filter((row) => row[0]); // Filter out empty rows

  // Transform data into the desired format
  const playerData = {};
  let stopProcessing = false;

  // Process each day's data (columns)
  for (let col = 1; col < headers.length; col++) {
    if (stopProcessing) break;

    const currentDayData = dataRows.map((row) => {
      return parseFloat(row[col]?.toString().replace('€', '').replace(',', '').trim()) || 0;
    }).map((value) => parseFloat(value.toFixed(2))); // Round to two decimals

    if (col > 1) {
      // Compare current day data to the previous day data
      const previousDayData = dataRows.map((row) => {
        return parseFloat(row[col - 1]?.toString().replace('€', '').replace(',', '').trim()) || 0;
      }).map((value) => parseFloat(value.toFixed(2))); // Round to two decimals

      const isIdentical = currentDayData.every((val, idx) => val === previousDayData[idx]);

      if (isIdentical) {
        stopProcessing = true;
        break;
      }
    }

    // Update player data
    dataRows.forEach((row, idx) => {
      const playerName = row[0];
      if (!playerData[playerName]) {
        playerData[playerName] = [];
      }
      playerData[playerName].push(currentDayData[idx]);
    });
  }

  // Calculate the number of days based on the number of elements in the first player's data array
  const firstPlayerData = playerData[Object.keys(playerData)[0]];
  const numberOfDays = firstPlayerData ? firstPlayerData.length : 0; // Number of days corresponds to the length of data for the first player
  const categories = Array.from({ length: numberOfDays }, (_, index) => `Day ${index}`);

  // Convert the playerData object to the desired format
  const lineChartDataDashboard = Object.entries(playerData).map(([name, data]) => {
    return { name, data };
  });

  // Read the options file and update categories
  const optionsFileContent = fs.readFileSync(optionsFilePath, 'utf-8');

  // Replace the categories part of the options with the generated days
  const updatedOptionsFileContent = optionsFileContent.replace(
    /categories: \[.*?\],/s, // Regex to match the existing categories array
    `categories: ${JSON.stringify(categories, null, 2)},`
  );

  // Write the updated content back to the options file
  fs.writeFileSync(optionsFilePath, updatedOptionsFileContent);
  console.log(`Options file successfully updated with days in ${optionsFilePath}`);

  // Optionally: Save the player data to the specified JS file
  const jsFileContent = fs.readFileSync(jsFilePath, 'utf-8');
  const updatedJsFileContent = jsFileContent.replace(
    /export const lineChartDataDashboard = \[.*?\];/s, // Regex to match the existing array
    `export const lineChartDataDashboard = ${JSON.stringify(lineChartDataDashboard, null, 2)};`
  );

  // Write the updated content back to the JS file
  fs.writeFileSync(jsFilePath, updatedJsFileContent);
  console.log(`lineChartDataDashboard successfully updated in ${jsFilePath}`);
}

// Example usage
const excelFilePath = './../../../../../Poker_Chip_Tracker.xlsx'; // Path to your Excel file
const jsFilePath = './lineChartData.js'; // Path to your JavaScript file containing player data
const optionsFilePath = './lineChartOptions.js'; // Path to the file containing the chart options
updateLineChartDataDashboard(excelFilePath, jsFilePath, optionsFilePath);
