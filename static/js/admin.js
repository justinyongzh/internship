document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.reject').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent the default form submission
            
            // Retrieve the 'company_id' from the data attribute
            var companyID = button.getAttribute('data-companyID');
            
            // Send a POST request to the server to delete the company
            fetch('/delete_company', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'company_id=' + companyID, // Include the company ID in the request
            })
            .then(function(response) {
                if (response.ok) {
                    // Company deleted successfully, now update the table
                    return response.json(); // Parse the JSON response
                } else {
                    // Handle errors or display an error message
                    console.error('Error deleting company. Status:', response.status);
                    response.text().then(function(errorMessage) {
                        console.error('Error Message:', errorMessage);
                    });
                }
            })
            .then(function(data) {
                // Update the table with the new data
                renderTable(data);
            })
            .catch(function(error) {
                console.error('Fetch Error:', error);
            });
        });
    });

    console.log('DOMContentLoaded event is firing.');
    document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.approve').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent the default form submission
            
            // Retrieve the 'company_id' from the data attribute
            var companyID = button.getAttribute('data-companyID');
            
            // Send a POST request to the server to update the company status
            fetch('/update_company_status', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'company_id=' + companyID, // Include the company ID in the request
            })
            .then(function(response) {
                if (response.ok) {
                    // Company approved successfully, now update the table
                    console.log('Approve Company ID:', companyID);
                    return response.json(); // Parse the JSON response
                } else {
                    // Handle errors or display an error message
                    console.error('Error approving company. Status:', response.status);
                    response.text().then(function(errorMessage) {
                        console.error('Error Message:', errorMessage);
                    });
                }
            })
            .then(function(data) {
                // Update the table with the new data
                renderTable(data);
            })
            .catch(function(error) {
                console.error('Fetch Error:', error);
            });
        });
    });
});

    
    function renderTable(data) {
    // Assuming you have a table element with ID 'companyTable'
    var table = document.getElementById('companyTable');

    // Clear the existing table rows, excluding the header row
    var rowCount = table.rows.length;
    for (var i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
    }

    // Iterate over the updated data and add rows to the table
    data.data.forEach(function (row) {
        var newRow = table.insertRow(-1);

        // Add cells and data for each column
        var cell1 = newRow.insertCell(0); // Company ID
        cell1.classList.add('table', 'td'); // Add appropriate classes
        var cell2 = newRow.insertCell(1); // Company Name
        cell2.classList.add('table', 'td'); // Add appropriate classes
        var cell3 = newRow.insertCell(2); // Address
        cell3.classList.add('table', 'td'); // Add appropriate classes
        var cell4 = newRow.insertCell(3); // Contact No.
        cell4.classList.add('table', 'td'); // Add appropriate classes
        var cell5 = newRow.insertCell(4); // Email
        cell5.classList.add('table', 'td'); // Add appropriate classes
        var cell6 = newRow.insertCell(5); // Action
        
        // Set data in the cells
        cell1.innerHTML = row[0];
        cell2.innerHTML = row[1];
        cell3.innerHTML = row[2];
        cell4.innerHTML = row[3];
        cell5.innerHTML = row[4];

        // Assuming you have buttons for each row similar to your HTML
        cell6.innerHTML = '<div class="button-group-area mt-10">' +
            '<button class="genric-btn success circle arrow">Approve</button>' +
            '<button class="genric-btn success circle arrow reject" data-companyID="' + row[0] + '">Reject</button>' +
            '</div>';
        
        // The background colors for <td> elements will be maintained automatically
        // based on your existing CSS
    });
}
});
