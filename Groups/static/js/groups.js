const url = "http://127.0.0.1:8000/api/groups"

let groups = [];

function processResponse(response) {
	return new Promise((resolve, reject) => {
		let func;
		response.status < 400 ? func = resolve : func = reject;
		response.json().then(data => func({'status': response.status, 'data': data}));
	});
}


function errorsToString(data){
	var errors = "";
	for (var field in data){
		errors += '"' + field + '": ' + data[field] + '\n';
	}
	return errors;
}


function getGroups(){
	var requestOptions = {
  		method: 'GET',
  		headers: {
			'Content-Type': 'application/json'
		}
	};
	fetch(url, requestOptions)
	  .then(response => response.json())
	  .then(data => _displayGroups(data))
	  .catch(error => console.log('error', error));
}


function addGroup(){
	const addNameTextbox = document.getElementById('add-name');
	const addFacultyTextbox = document.getElementById('add-faculty');

	var name = addNameTextbox.value.trim();
	var faculty = addFacultyTextbox.value.trim();

	var raw = JSON.stringify({
		"name":name,
		"faculty":faculty});

	var requestOptions = {
  		method: 'POST',
  		headers: {
  			'Content-Type': 'application/json'
  		},
  		body: raw
	};

	fetch(url, requestOptions)
		.then(processResponse)
  		.then(response => {
        	getGroups();
        	addNameTextbox.value = '';
      		addFacultyTextbox.value = '';
      	})
  		.catch(response => {
        	alert(errorsToString(response.data));
      	});
}


function deleteGroup(id) {
	if (!confirm(`Delete group with id=${id}?`))
		return;

	var requestOptions = {
  		method: 'DELETE',
  		redirect: 'follow'
	};

	fetch(`${url}${id}`, requestOptions)
  		.then(response => response.text())
  		.then(result => getGroups())
  		.catch(error => console.log('error', error));
}


function displayEditForm(id) {
    const group = groups.find(group => group.id === id);
    document.getElementById('edit-id').value = genre.id;
    document.getElementById('edit-name').value = genre.name;
    document.getElementById('edit-faculty').value = genre.faculty;
    document.getElementById('editForm').style.display = 'block';
}


function updateGroup(){
	const groupId = document.getElementById('edit-id').value;
	const groupName = document.getElementById('edit-name').value;
	const groupFaculty = document.getElementById('edit-faculty').value;

	const updateNameTextBox = document.getElementById('edit-name');
	const updateFacultyTextBox = document.getElementById('edit-faculty');

	if (!confirm(`Edit group with id=${groupId}?`))
		return;
	var raw = JSON.stringify({
		"id": groupId,
		"name": groupName,
		"faculty": groupFaculty
	});

	var requestOptions = {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
	  	},
	  	body: raw
	};

	fetch(`${url}${groupId}`, requestOptions)
	 	.then(processResponse)
  		.then(response => {
        	getGroups();
        	updateNameTextBox.value = '';
        	updateFacultyTextBox.value = '';
      	})
  		.catch(response => {
        	alert(errorsToString(response.data));
      	});
}

function _displayGroups(data) {
   	const tBody = document.getElementById('groups');
    tBody.innerHTML = '';
 
    const button = document.createElement('button');
    data.forEach(group => {
        let editButton = button.cloneNode(false);
        editButton.innerText = 'Edit';
        editButton.setAttribute('onclick', `displayEditForm(${group.id})`);
		editButton.setAttribute('class', `button buttonEdit`);

        let deleteButton = button.cloneNode(false);
        deleteButton.innerText = 'Delete';
        deleteButton.setAttribute('onclick', `deleteGroup(${group.id})`);
        deleteButton.setAttribute('class', `button buttonDelete`);

		let tr = tBody.insertRow();

		let td1 = tr.insertCell(0);
		let textNodeId = document.createTextNode(group.id);
    	td1.appendChild(textNodeId);   

		let td2 = tr.insertCell(1);
        let textNodeName = document.createTextNode(group.name);
        td2.appendChild(textNodeName);

		let td3 = tr.insertCell(2);
        let textNodeInfo = document.createTextNode(group.faculty);
        td3.appendChild(textNodeInfo);

		let td4 = tr.insertCell(3);
        td4.appendChild(editButton);

        let td5 = tr.insertCell(4);
        td5.appendChild(deleteButton);
    });
    groups = data;
}
