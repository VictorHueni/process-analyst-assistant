function sendMessage() {
  let input = document.getElementById("userInput");
  let message = input.value.trim(); // Remove leading/trailing white spaces

  // Check if message is not empty
  if (message === "") {
    alert("Please enter a message.");
    return; // Exit the function
  }

  displayMessage(message, "user");
  input.value = ""; // Clear input box

  // Make a GET request to the /query endpoint with the user input as a query parameter
  fetch(`/query?text=${encodeURIComponent(message)}`)
    .then(response => response.text())
    .then(data => {
      // Display the response from the server
      displayMessage(data, "bot");
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function displayMessage(message, sender) {
  let messageDiv = document.createElement("div");
  messageDiv.textContent = message;
  messageDiv.className = "message-" + sender;
  document.getElementById("conversation").appendChild(messageDiv);
}

function selectProcedure() {
  const procedure = document.getElementById("procedure").value;
  let message = "Vous avez choisi la procédure " + procedure + ".";
  displayMessage(message, "bot");
}

  let diagramUrl = 'https://cdn.statically.io/gh/bpmn-io/bpmn-js-examples/dfceecba/starter/diagram.bpmn'; //"./static/media/05-test-prep-dishes-working.bpmn"; //'https://cdn.statically.io/gh/bpmn-io/bpmn-js-examples/dfceecba/starter/diagram.bpmn';
const bpmnViewer = new BpmnJS({ container: "#canvas" });

/**
 * Open diagram in our viewer instance.
 *
 * @param {String} bpmnXML diagram to display
 */
async function openDiagram(bpmnXML) {
  // import diagram
  try {
    await bpmnViewer.importXML(bpmnXML);

    // access viewer components
    let canvas = bpmnViewer.get("canvas");
    let overlays = bpmnViewer.get("overlays");

    // zoom to fit full viewport
    canvas.zoom("fit-viewport");

    // attach an overlay to a node
    overlays.add("SCAN_OK", "note", {
      position: {
        bottom: 0,
        right: 0,
      },
      html: '<div class="diagram-note">Mixed up the labels?</div>',
    });

    // add marker
    canvas.addMarker("SCAN_OK", "needs-discussion");
  } catch (err) {
    console.error("could not import BPMN 2.0 diagram", err);
  }
}

// load external diagram file via AJAX and open it
$.get(diagramUrl, openDiagram, "text");

$(document).ready(function(){
    $('#fileDropdown').change(function(){
        let selectedFile = $(this).val();
        $.ajax({
            url: '/get_file_content',
            data: {'file': selectedFile},
            type: 'GET',
            success: function(response){
                // Use the response to update the canvas
                openDiagram(response).then(r => console.log("Diagram loaded"));
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});

