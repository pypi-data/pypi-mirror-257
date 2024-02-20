import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';


import { plotElements } from './ieHelper.js';
import {ObliqueCylinderGeometry} from './obliqueCylinder.js';
import {TrapezoidGeometry} from './trapezoid.js'
import {generateBeam} from './geometryHelper.js';
import {glToJson, jsonToGl} from './translationHelper.js';
import { builderColours, addColourFolders, contextualColours, materialColours, geometryColours,
	     cElements, materialColourKeys, contextualColourKeys, resetColour, resetColours,
	     makeContextColourVisible, makeMaterialColourVisible, makeGeometryColourVisible, otherColours} from './colourHelper.js';


const canvas = document.querySelector('#c');
let camera, scene, renderer, controls;
let floor;
let pointer, raycaster, isShiftDown = false, isCtrlDown = false;


// Gui handlers
const gui = new GUI();
addColourFolders(gui, render, "builder");


// Folder for defining objects between elements
let selectedObjects = new Array(2); // Selecting objects for relationships
let relationships = {};
const relationFolder = gui.addFolder('Relationships');
const elRelationship = {'Relationship': 'none'}  // current relationship type selected
const relationshipTypes = {'free': ['none', 'perfect', 'connection', 'joint'],
'grounded': ['none', 'perfect', 'connection', 'joint', 'boundary']};
const showElements = {'Show orphans': false, 'Hide connected': false};
relationFolder.add(showElements, 'Show orphans',).onChange(value => toggleHighlightUnrelated(value));
relationFolder.addColor(otherColours, 'Orphans');
relationFolder.add(showElements, 'Hide connected',).onChange(value => toggleHideConnected(value));
relationFolder.add(elRelationship, 'Relationship', relationshipTypes['free']).onChange( value => updateRelationship(value));
relationFolder.add(elRelationship, 'Relationship', relationshipTypes['grounded']).onChange( value => updateRelationship(value));
relationFolder.children[3].hide();
relationFolder.children[4].hide();



const elementFolder = gui.addFolder('Element');
const elInfo = {'Name': '', 'Is ground': false}
elementFolder.add(elInfo, 'Name').onChange(updateElementName);
elementFolder.add(elInfo, 'Is ground',).onChange(value => toggleGround(value));
elementFolder.hide();
let floorFolder, boxFolder, sphereFolder, cylinderFolder, obliqueCylinderFolder, trapezoidFolder, beamFolder, folders, currentFolder;



// Coordinates folders
const posParams = {'x': 0,
  				   'y': 0,
				   'z': 0};
const rotateParams = {'x': 0,
					  'y': 0,
					  'z': 0}
const coordsFolder = elementFolder.addFolder('Coordinates');
const transFolder = coordsFolder.addFolder('Translational');
const rotFolder = coordsFolder.addFolder('Rotational');
transFolder.add(posParams, 'x').onChange(moveGeometryX);
transFolder.add(posParams, 'y').onChange(moveGeometryY);
transFolder.add(posParams, 'z').onChange(moveGeometryZ);
rotFolder.add(rotateParams, 'x', 0, 360).onChange(rotateGeometryX);
rotFolder.add(rotateParams, 'y', 0, 360).onChange(rotateGeometryY);
rotFolder.add(rotateParams, 'z', 0, 360).onChange(rotateGeometryZ);

// Material information
const material = {"Type": "other"};
const materialFolder = elementFolder.addFolder('Material');
materialFolder.add(material, 'Type', materialColourKeys).onChange(updateMaterial);


// Contextual information
const context = {'Type': 'other'};
const contextualFolder = elementFolder.addFolder('Contextual');
contextualFolder.add(context, 'Type', contextualColourKeys).onChange(updateContext);


// Geometry information
const geometry = {"Type": undefined}
const jsonGeometryMappings = {"box": ["solid-translate-cuboid", "shell-translate-cuboid",
                                       "solid-translate-other", "shell-translate-other", "other"], 
                              "sphere": ["solid-translate-sphere", "shell-translate-sphere",
                                         "solid-translate-other", "shell-translate-other", "other"], 
                              "cylinder": ["solid-translate-cylinder", "shell-translate-cylinder",
                                           "solid-translate-other", "shell-translate-other", "other"], 
                              "beam": ["beam-rectangular", "beam-i-beam", "beam-other", "other"], 
                              "trapezoid": ["solid-translateAndScale-cuboid", "shell-translateAndScale-cuboid",
                                            "solid-translateAndScale-other", "shell-translateAndScale-other", "other"], 
                              "obliqueCylinder": ["solid-translateAndScale-cylinder", "shell-translateAndScale-cylinder",
                                                  "solid-translateAndScale-other", "shell-translateAndScale-other", "other"]};
const geometryKeys = Object.keys(jsonGeometryMappings);
geometryKeys.sort();
const geometryFolder = elementFolder.addFolder('Geometry');
for (let i=0; i<geometryKeys.length; i++){
	geometryFolder.add(geometry, 'Type', jsonGeometryMappings[geometryKeys[i]]).onChange(updateJsonGeometry);
	geometryFolder.children[i].hide();
}
geometryFolder.hide();


// Geometry folders
const floorParams = {'width': 300,
					 'depth': 300};
const boxParams = {'length': 5,
                   'height': 5,
				   'width': 5};
const sphereParams = {'radius': 3}
const cylinderParams = {'radius': 3,
   			   		    'length': 5}
const obliqueCylinderParams = {'Faces left radius': 3,
   			   		    	   'Faces right radius': 3,
							   'Faces Left Trans. y': 0,
							   'Faces Left Trans. z': 0,
							   'Faces Right Trans. y': 0,
							   'Faces Right Trans. z': 0,
 							   'length': 5}
const trapezoidParams = {"Faces Left Trans. y": 3,
						 "Faces Left Trans. z": 3,
						 "Faces Left Height": 2,
						 "Faces Left Width": 2,
						 "Faces Right Trans. y": 0,
						 "Faces Right Trans. z": 0,
						 "Faces Right Height": 4,
						 "Faces Right Width": 4,
						 "length": 5}
const beamParams = {"length": 8,
				    "h": 4,
				    "s": 1,
				    "t": 1,
				    "b": 3}



let rollOverMesh;
const rollOverMaterial = new THREE.MeshBasicMaterial( { color: 0xff0000, opacity: 0.5, transparent: true } );
const rollOverCubeGeo = new THREE.BoxGeometry(boxParams.length, boxParams.height, boxParams.width);
const rollOverSphereGeo = new THREE.SphereGeometry(sphereParams.radius);
const rollOverCylinderGeo = new THREE.CylinderGeometry(cylinderParams.radius, cylinderParams.radius, cylinderParams.length);
const rollOverObliqueCylinderGeo = new ObliqueCylinderGeometry(obliqueCylinderParams['Faces left radius'],
															   obliqueCylinderParams['Faces left radius'],
															   obliqueCylinderParams.length,
															   obliqueCylinderParams['Faces Right Trans. y']  - obliqueCylinderParams['Faces Left Trans. y'] ,
															   -(obliqueCylinderParams['Faces Right Trans. z']  - obliqueCylinderParams['Faces Left Trans. z']));
const rollOverTrapezoidGeo = new TrapezoidGeometry(trapezoidParams['Faces Left Trans. y'], trapezoidParams['Faces Left Trans. z'],
												   trapezoidParams['Faces Left Height'], trapezoidParams['Faces Left Width'],
												   trapezoidParams['Faces Right Trans. y'], trapezoidParams['Faces Right Trans. z'],
												   trapezoidParams['Faces Right Height'], trapezoidParams['Faces Right Width'],
												   trapezoidParams.length);
const rollOverIBeamGeo = generateBeam("i-beam", beamParams.length, beamParams.h, beamParams.s, beamParams.t, beamParams.b);
const rollOverCBeamGeo = generateBeam("c-beam", beamParams.length, beamParams.h, beamParams.s, beamParams.t, beamParams.b);
rollOverCylinderGeo.rotateZ(Math.PI/2);
rollOverObliqueCylinderGeo.rotateZ(Math.PI/2);
let planeGeometry;

let currentId;  // name of the new geometry object to be added
let currentGeometry;
let currentObject;  // specific existing object to be edited
const objects = [];  // list of all objects in the scene


function loadBlankBuilder(){
	camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
	camera.position.set( 0, 100, 300 );
	camera.lookAt( 0, 0, 0 );

	// Give the user the ability to control the camera
	controls = new OrbitControls(camera, renderer.domElement);
	controls.target.set(0, 0, 0);	// where the camera looks
	// Only render when the user moves the camera
	controls.addEventListener("change", () => renderer.render(scene, camera));
	controls.update();

	// Draw the floor
	planeGeometry = new THREE.PlaneGeometry(floorParams.width, floorParams.depth );
	planeGeometry.rotateX( - Math.PI / 2 );
	floor = new THREE.Mesh( planeGeometry, new THREE.MeshBasicMaterial( { visible: true } ) );
	floor.name = "plane";
	scene.add( floor );
	objects.push( floor );

	// Lights
	const ambientLight = new THREE.AmbientLight( 0x606060, 3 );
	scene.add( ambientLight );

	const directionalLight = new THREE.DirectionalLight( 0xffffff, 3 );
	directionalLight.position.set( 1, 0.75, 0.5 ).normalize();
	scene.add( directionalLight );

}


function buildModel(shapes=undefined) {
	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0xf0f0f0 );
	
	renderer = new THREE.WebGLRenderer( { antialias: true }, canvas );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );
		
	let info;
	if (shapes == undefined) {
		loadBlankBuilder();
	} else {
		info = plotElements(renderer.domElement, scene, shapes);
		camera = info.camera
		for (let e of info.elements) {
			cElements.push(e);
			objects.push(e)
			e.currentAngleX = 0;
			e.currentAngleY = 0;
			e.currentAngleZ = 0;
			if (e.el_contextual != "ground") {
				makeContextColourVisible(e.el_contextual);
				makeMaterialColourVisible(e.el_material);
				makeGeometryColourVisible(e.el_geometry);
			}
		}
		resetColours(gui.children[0].children[0].getValue());
		controls = info.controls;
		floor = info.floor;
		objects.push(floor);
	}


		// Only render when the user moves the camera
		controls.addEventListener("change", () => renderer.render(scene, camera));
		controls.update();
	
	
	// Roll-over helpers
	rollOverMesh = new THREE.Mesh(rollOverIBeamGeo, rollOverMaterial);
	rollOverMesh.visible = false;
	scene.add( rollOverMesh );

	// To detect where the user has clicked
	raycaster = new THREE.Raycaster();
	pointer = new THREE.Vector2();


	document.addEventListener( 'pointermove', onPointerMove );
	document.addEventListener( 'pointerdown', onPointerDown );
	document.addEventListener( 'keydown', onDocumentKeyDown );
	document.addEventListener( 'keyup', onDocumentKeyUp );
	
	document.querySelectorAll( '#ui .tiles input[type=radio][name=voxel]' ).forEach( ( elem ) => {
		elem.addEventListener( 'click', allowUncheck );
	} );
	document.querySelectorAll( '#uitwo .tiles input[type=radio][name=voxel]' ).forEach( ( elem ) => {
		elem.addEventListener( 'click', allowUncheck );
	} );

	window.addEventListener( 'resize', onWindowResize );

	
	initBoxGui()
	initSphereGui();
	initCylinderGui();
	initObliqueCylinderGui();
	initTrapezoidGui();
	initBeamGui();
	initGroundGui();  // Not added to list of folders so it is always visible
	folders = [boxFolder, sphereFolder, cylinderFolder, obliqueCylinderFolder, trapezoidFolder, beamFolder];
	folders.forEach(folder => folder.hide()); // Initially hide all folders, then show only the ones we want when required
	render();
}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize( window.innerWidth, window.innerHeight );
	render();
}


function onPointerMove( event ) {
	if (currentId != undefined){
		pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 );
		raycaster.setFromCamera( pointer, camera );
		const intersects = raycaster.intersectObjects( objects, false );
		rollOverMesh.geometry.computeBoundingBox();
		const rollOverHeight = (rollOverMesh.geometry.boundingBox.max.z - rollOverMesh.geometry.boundingBox.min.z) / 2
		if ( intersects.length > 0 ) {
			const intersect = intersects[ 0 ];
			rollOverMesh.position.copy( intersect.point ).add( intersect.face.normal );
			rollOverMesh.position.addScalar(rollOverHeight);
			render();
		}
	}
}


function onPointerDown( event ) {
	pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 );
	raycaster.setFromCamera( pointer, camera );
	const intersects = raycaster.intersectObjects( objects, false );
	if ( intersects.length > 0 ) {
		const intersect = intersects[ 0 ];
		if ( isShiftDown ) {
			// delete object
			if ( intersect.object !== floor ) {
				scene.remove( intersect.object );
				objects.splice( objects.indexOf( intersect.object ), 1 );
				cElements.splice( cElements.indexOf( intersect.object ), 1 );
			}
		} else if ( isCtrlDown ) {
			// select object
			elementFolder.hide();
			if ( intersect.object !== floor ) {
				if (selectedObjects[0] == intersect.object) {
					// If it was already object 0, deselect it
					resetColour(gui.children[0].children[0].getValue(), intersect.object);
					// Move object 1 to first place
					selectedObjects[0] = selectedObjects[1];
					selectedObjects[1] = undefined;
					relationFolder.children[3].hide();
					relationFolder.children[4].hide();
				} else if (selectedObjects[1] == intersect.object) {	
					// If it was already object 1, deselect it
					resetColour(gui.children[0].children[0].getValue(), intersect.object);
					selectedObjects[1] = undefined;
					relationFolder.children[3].hide();
					relationFolder.children[4].hide();
				} else {
					// Otherwise, select it
					intersect.object.material.color.setHex(otherColours['Selected element']);
					if (selectedObjects[0] == undefined) { 
						// Assign as object 0 if the space was free
						selectedObjects[0] = intersect.object;
					} else {
						if (selectedObjects[1] != undefined) {	
							// If two objects are already selected, deselect object 1 (i.e. reset its colour)
							resetColour(gui.children[0].children[0].getValue(), selectedObjects[1]);
						}
						// Assign as object 1
						selectedObjects[1] = intersect.object;
						// Two elements are selected so (if they are both named) show the dropdown menu to select their relationship
						if (selectedObjects[0].name.length > 0 && selectedObjects[1].name.length > 0) {
							// Show the current relationship they have
							const currentRelat = currentRelationship(selectedObjects[0].name, selectedObjects[1].name);
							relationFolder.show();
							if (selectedObjects[0].el_contextual == "ground" || selectedObjects[1].el_contextual == "ground"){
								relationFolder.children[3].hide();  // hide 'free' relationships folder
								relationFolder.children[4].show();  // show 'grounded' relationships folder
								relationFolder.children[4].setValue(currentRelat);
							} else {
								relationFolder.children[3].show();  // show 'free'
								relationFolder.children[3].setValue(currentRelat);
								relationFolder.children[4].hide();  // hide 'grounded'
							}
						}
					}
				}
			}
		} else {
			if (currentId != undefined){
				// Add new object
				if (currentId == "cube"){
					currentGeometry = new THREE.BoxGeometry(boxParams.length, boxParams.height, boxParams.width);;
				} else if (currentId == "sphere"){
					currentGeometry = new THREE.SphereGeometry(sphereParams.radius);;
				} else if (currentId == "cylinder"){
					currentGeometry = new THREE.CylinderGeometry(cylinderParams.radius, cylinderParams.radius, cylinderParams.length);;
					// Rotate because cylinder is assumed horizontal in json but vertical in webGL
					currentGeometry.rotateZ(Math.PI/2);
				} else if (currentId == "obliqueCylinder"){
					currentGeometry = new ObliqueCylinderGeometry(obliqueCylinderParams['Faces left radius'],
						obliqueCylinderParams['Faces right radius'],
						obliqueCylinderParams.length,
						obliqueCylinderParams['Faces Right Trans. y']  - obliqueCylinderParams['Faces Left Trans. y'] ,
						-(obliqueCylinderParams['Faces Right Trans. z']  - obliqueCylinderParams['Faces Left Trans. z']));
					currentGeometry.parameters['Faces Left Trans. y'] = obliqueCylinderParams['Faces Left Trans. y']
					currentGeometry.parameters['Faces Left Trans. z'] = obliqueCylinderParams['Faces Left Trans. z']
					currentGeometry.parameters['Faces Right Trans. y'] = obliqueCylinderParams['Faces Right Trans. y']
					currentGeometry.parameters['Faces Right Trans. z'] = obliqueCylinderParams['Faces Right Trans. z']
					// Rotate because cylinder is assumed horizontal in json but vertical in webGL
					currentGeometry.rotateZ(Math.PI/2);
				} else if (currentId == "trapezoid"){
					currentGeometry = new TrapezoidGeometry(10, 10, 20, 20, 0, 0, 40, 40, 50);
				} else if (currentId == "ibeam"){
					currentGeometry = generateBeam("i-beam", beamParams.length, beamParams.h, beamParams.s, beamParams.t, beamParams.b);;
				} else if (currentId == "cbeam"){
					currentGeometry = generateBeam("c-beam", beamParams.length, beamParams.h, beamParams.s, beamParams.t, beamParams.b);;
				}

				// create new object
				const voxel = new THREE.Mesh(currentGeometry, new THREE.MeshLambertMaterial({color: builderColours[currentGeometry.type]}));
				voxel.position.copy( intersect.point ).add( intersect.face.normal );
				// Find the size of the geometry in the y-axis and raise it so it's not half-way through the floor
				voxel.geometry.computeBoundingBox()
				voxel.position.addScalar((voxel.geometry.boundingBox.max.z - voxel.geometry.boundingBox.min.z)/2);
				// We need to know the current angle so that when we change the object's angle we don't
				// have a cumulative effect of rotations for each rotation we make.
				voxel.currentAngleX = 0;
				voxel.currentAngleY = 0;
				voxel.currentAngleZ = 0;
				voxel.contextual_type = undefined;
				voxel.material_type = undefined;
				voxel.relationshipCount = 0;
				scene.add( voxel );
				objects.push( voxel );
				currentObject = voxel;
				cElements.push(voxel);
			} else {
				// select existing object to edit unless it's the floor
				if (intersect.object.name != "plane") {
					currentObject = intersect.object;
				}
			}
			folders.forEach(folder => folder.hide());
			const geometryType = currentObject.geometry.type;
			if (geometryType == "BoxGeometry"){
				boxFolder.children[0].setValue(currentObject.geometry.parameters.width);
				boxFolder.children[1].setValue(currentObject.geometry.parameters.height);
				boxFolder.children[2].setValue(currentObject.geometry.parameters.depth);
				currentFolder = boxFolder;
				showGeometryDropdown("box");
			} else if (geometryType == "SphereGeometry"){
				sphereFolder.children[0].setValue(currentObject.geometry.parameters.radius);
				currentFolder = sphereFolder;
				showGeometryDropdown("sphere");
			} else if (geometryType == "CylinderGeometry"){
				cylinderFolder.children[0].setValue(currentObject.geometry.parameters.radiusTop);
				cylinderFolder.children[1].setValue(currentObject.geometry.parameters.height);
				currentFolder = cylinderFolder;
				showGeometryDropdown("cylinder");
			} else if (geometryType == "ObliqueCylinderGeometry"){
				obliqueCylinderFolder.children[0].setValue(currentObject.geometry.parameters.radiusTop);
				obliqueCylinderFolder.children[1].setValue(currentObject.geometry.parameters.radiusBottom);
				obliqueCylinderFolder.children[2].setValue(currentObject.geometry.parameters.height);
				obliqueCylinderFolder.children[3].setValue(currentObject.geometry.parameters['Faces Left Trans. y']);
				obliqueCylinderFolder.children[4].setValue(currentObject.geometry.parameters['Faces Left Trans. z']);
				obliqueCylinderFolder.children[5].setValue(currentObject.geometry.parameters['Faces Right Trans. y']);
				obliqueCylinderFolder.children[6].setValue(currentObject.geometry.parameters['Faces Right Trans. z']);
				currentFolder = obliqueCylinderFolder;
				showGeometryDropdown("obliqueCylinder");
			} else if  (geometryType == "TrapezoidGeometry"){
				trapezoidFolder.children[0].setValue(currentObject.geometry.parameters.leftTransY);
				trapezoidFolder.children[1].setValue(currentObject.geometry.parameters.leftTransZ);
				trapezoidFolder.children[2].setValue(currentObject.geometry.parameters.leftDimensY);
				trapezoidFolder.children[3].setValue(currentObject.geometry.parameters.leftDimensZ);
				trapezoidFolder.children[4].setValue(currentObject.geometry.parameters.rightTransY);
				trapezoidFolder.children[5].setValue(currentObject.geometry.parameters.rightTransZ);
				trapezoidFolder.children[6].setValue(currentObject.geometry.parameters.rightDimensY);
				trapezoidFolder.children[7].setValue(currentObject.geometry.parameters.rightDimensZ);
				trapezoidFolder.children[8].setValue(currentObject.geometry.parameters.width);
				currentFolder = trapezoidFolder;
				showGeometryDropdown("trapezoid");
			} else if (geometryType == "IBeamGeometry" || geometryType == "CBeamGeometry"){
				beamFolder.children[0].setValue(currentObject.geometry.parameters["width"]);
				beamFolder.children[1].setValue(currentObject.geometry.parameters["h"]);
				beamFolder.children[2].setValue(currentObject.geometry.parameters["s"]);
				beamFolder.children[3].setValue(currentObject.geometry.parameters["t"]);
				beamFolder.children[4].setValue(currentObject.geometry.parameters["b"]);
				currentFolder = beamFolder;
				showGeometryDropdown("beam");
			} else {
				// Need to deselect if we click away so we don't accidentally edit something else (e.g. the plane)
				currentFolder = undefined;
			}
			// If the ground plane has been selected, or anywhere outside of this then there'll be no current folder.
			if (currentFolder != undefined){
				elementFolder.children[0].setValue(currentObject.name);
				transFolder.children[0].setValue(glToJson(currentObject, "x", currentObject.position.x));
				transFolder.children[1].setValue(glToJson(currentObject, "y", currentObject.position.y));
				transFolder.children[2].setValue(glToJson(currentObject, "z", currentObject.position.z));
				rotFolder.children[0].setValue(currentObject.rotation.x * (180 / Math.PI));
				rotFolder.children[1].setValue(currentObject.rotation.y * (180 / Math.PI));
				rotFolder.children[2].setValue(currentObject.rotation.z * (180 / Math.PI));
				materialFolder.children[0].setValue(currentObject.el_material);
				if (currentObject.el_contextual == 'ground'){
					elementFolder.children[1].setValue(true);
				} else {
					contextualFolder.children[0].setValue(currentObject.el_contextual);
					elementFolder.show();
					coordsFolder.show();
					contextualFolder.show();
					materialFolder.show();
					currentFolder.show();
					elementFolder.children[1].setValue(false);
				}
			}
		}
	}
	render();
}


function onDocumentKeyDown( event ) {
	switch ( event.keyCode ) {
		case 16: isShiftDown = true; break;
		case 17: isCtrlDown = true; break;
		// case 37:  // left
		// 	currentFolder.children[0].setValue(currentObject.position.x - 10);
		// 	break;
		// case 38:  // up
		// 	currentFolder.children[2].setValue(currentObject.position.z - 10);
		// 	break;
		// case 39:  // right
		// 	currentFolder.children[0].setValue(currentObject.position.x + 10);
		// 	break;
		// case 40:  // down
		// 	currentFolder.children[2].setValue(currentObject.position.z + 10);
		// 	break;
		// case 83:  // s
		// 	currentFolder.children[1].setValue(currentObject.position.y - 10);
		// 	break;
		// case 87:  // w
		// 	currentFolder.children[1].setValue(currentObject.position.y + 10);
		// 	break;
	}
	render();
}


function onDocumentKeyUp( event ) {
	switch ( event.keyCode ) {
		case 16: isShiftDown = false; break;
		case 17: isCtrlDown = false; break;
	}
}


function allowUncheck() {
	if ( this.id === currentId ) {
		this.checked = false;
		currentId = undefined;
		rollOverMesh.visible = false;
	} else {
		currentId = this.id;
		rollOverMesh.geometry.dispose()
		if (currentId == "cube"){
			rollOverMesh.geometry = rollOverCubeGeo;
			currentFolder = boxFolder;
		} else if (currentId == "sphere"){
			rollOverMesh.geometry = rollOverSphereGeo;
			currentFolder = sphereFolder;
		} else if (currentId == "cylinder"){
			rollOverMesh.geometry = rollOverCylinderGeo;
			currentFolder = cylinderFolder;	
		} else if (currentId == "obliqueCylinder"){
			rollOverMesh.geometry = rollOverObliqueCylinderGeo;
			currentFolder = obliqueCylinderFolder;
		} else if (currentId == "trapezoid"){
			rollOverMesh.geometry = rollOverTrapezoidGeo;
			currentFolder = trapezoidFolder;
		} else if (currentId == "ibeam"){
			rollOverMesh.geometry = rollOverIBeamGeo;
			currentFolder = beamFolder;
		} else if (currentId == "cbeam"){
			rollOverMesh.geometry = rollOverCBeamGeo;
			currentFolder = beamFolder;
		}
		rollOverMesh.visible = true;
	}
	folders.forEach(folder => folder.hide());
	
}

function updateGeometry(mesh, geometry){
	mesh.geometry.dispose();
	mesh.geometry = geometry;
	render();
}


function initGroundGui(){
	floorFolder = gui.addFolder('Ground dimensions (visual only)');
	floorFolder.add(floorParams, 'width').onChange(generateGeometry);
	floorFolder.add(floorParams, 'depth').onChange(generateGeometry);

	function generateGeometry(){
		planeGeometry = new THREE.PlaneGeometry( floorParams.width, floorParams.depth );
		planeGeometry.rotateX( - Math.PI / 2 );
		updateGeometry(floor, planeGeometry);
	}
}


function updateElementName(){
	currentObject.name = elInfo.Name;
}


function toggleGround(value){
	if (value == true){
		currentObject.el_contextual = 'ground';
		coordsFolder.hide();
		materialFolder.hide();
		contextualFolder.hide();
		geometryFolder.hide();
		folders.forEach(folder => folder.hide());  // hide all geometry dimension folders
		currentObject.material.color.setHex(otherColours.ground);
	} else {
		if (currentObject.el_contextual == 'ground') {
			// If it was ground then update it's context
			// This if-statement is needed because this function is also called for maintaining non-ground status.
			currentObject.el_contextual = undefined;
		}
		coordsFolder.show();
		materialFolder.show();
		contextualFolder.show();
		geometryFolder.show();
		if (currentObject.geometry.type == "BoxGeometry"){
			boxFolder.show();
		} else if (currentObject.geometry.type == "SphereGeometry"){
			sphereFolder.show();
		} else if (currentObject.geometry.type == "CylinderGeometry"){
			cylinderFolder.show();
		} else if (currentObject.geometry.type == "ObliqueCylinderGeometry"){
			obliqueCylinderFolder.show();
		} else if  (currentObject.geometry.type == "TrapezoidGeometry"){
			trapezoidFolder.show();
		} else if (currentObject.geometry.type == "IBeamGeometry" || geometry.type == "CBeamGeometry"){
			beamFolder.show();
		}
		if (currentObject.material.color.getHex() != otherColours['Orphans']
				&& currentObject.material.color.getHex() != otherColours['Selected element']) {
			// Don't change the colour if it's currently being highlighted as an orphan or selected element
			resetColour(gui.children[0].children[0].getValue(), currentObject);
		}
	}
	render();
}


// It's necessary to handle each dimension separately,
// otherwise the object's position attributes can get overwritten by whatever old values
// are in the gui before the gui has been updated to show the parameters.
// of the object that has just been selected.
function moveGeometryX(){
	currentObject.position.x = jsonToGl(currentObject, "x", posParams.x);
	currentObject.geometry.attributes.position.needsUpdate = true;
	render();
}


function moveGeometryY(){
	currentObject.position.y = jsonToGl(currentObject, "y", posParams.y);
	currentObject.geometry.attributes.position.needsUpdate = true;
	render();
}


function moveGeometryZ(){
	currentObject.position.z = jsonToGl(currentObject, "z", posParams.z);
	currentObject.geometry.attributes.position.needsUpdate = true;
	render();
}


function rotateGeometryX(){
	const newAngle = rotateParams.x * (Math.PI/180)
	const rotation = newAngle - currentObject.currentAngleX;
	currentObject.rotateX(rotation);
	currentObject.currentAngleX = newAngle;
	if (!currentObject.isGroup){
		currentObject.geometry.attributes.position.needsUpdate = true;
	}
	render();
}


function rotateGeometryY(){
	const newAngle = rotateParams.y * (Math.PI/180)
	const rotation = newAngle - currentObject.currentAngleY;
	currentObject.rotateY(rotation);
	currentObject.currentAngleY = newAngle;
	if (!currentObject.isGroup){
		currentObject.geometry.attributes.position.needsUpdate = true;
	}
	render();
}


function rotateGeometryZ(){
	const newAngle = rotateParams.z * (Math.PI/180)
	const rotation = newAngle - currentObject.currentAngleZ;
	currentObject.rotateZ(rotation);
	currentObject.currentAngleZ = newAngle;
	if (!currentObject.isGroup){
		currentObject.geometry.attributes.position.needsUpdate = true;
	}
	render();
}


function updateContext(){
	currentObject.el_contextual = context.Type;
	makeContextColourVisible(context.Type);
	if (gui.children[0].children[0].getValue() == "contextual"
			&& currentObject.material.color.getHex() != otherColours['Orphans']
			&& currentObject.material.color.getHex() != otherColours['Selected element']) {
		currentObject.material.color.setHex(contextualColours[currentObject.el_contextual]);
	}
	render();
}


function updateMaterial(){
	currentObject.el_material = material.Type;
	makeMaterialColourVisible(material.Type);
	if (gui.children[0].children[0].getValue() == "material"
			&& currentObject.material.color.getHex() != otherColours['Orphans']
			&& currentObject.material.color.getHex() != otherColours['Selected element']) {
		currentObject.material.color.setHex(materialColours[currentObject.el_material]);
	}
	render();
}


function updateJsonGeometry(){
	currentObject.el_geometry = geometry.Type;
	makeGeometryColourVisible(geometry.Type);
	if (gui.children[0].children[0].getValue() == "geometry"
			&& currentObject.material.color.getHex() != otherColours['Orphans']
			&& currentObject.material.color.getHex() != otherColours['Selected element']) {
		currentObject.material.color.setHex(geometryColours[currentObject.el_geometry]);
	}
	render();
}

function showGeometryDropdown(geom){
	// Hide whichever geometry dropdown is on display
	for (let i=0; i<geometryKeys.length; i++){
		geometryFolder.children[i].hide();
	}
	// Show the desired dropdown
	geometryFolder.show();
	const idx = geometryKeys.indexOf(geom)
	geometryFolder.children[idx].show();
	geometryFolder.children[idx].setValue(currentObject.el_geometry);
}


function initBoxGui(){
	boxFolder = elementFolder.addFolder('Geometry Dimensions');
	boxFolder.add(boxParams, 'length').onChange(value => updateParameters("width", value));
	boxFolder.add(boxParams, 'height').onChange(value => updateParameters("height", value));
	boxFolder.add(boxParams, 'width').onChange(value => updateParameters("depth", value));
	function updateParameters(changedParam, value){
		if (currentObject.geometry.parameters[changedParam] != value){  // don't regenerate to the object if we're just updating the gui
			const newParams = {...currentObject.geometry.parameters};
			newParams[changedParam] = value;
			updateGeometry(currentObject,
						new THREE.BoxGeometry(newParams.width, newParams.height, newParams.depth));
			if (changedParam == "height"){
				posParams.y = 0;
				moveGeometryY();
			}
		}
	}
}
  

function initSphereGui(){
	sphereFolder = elementFolder.addFolder('Geometry Dimensions');
	sphereFolder.add(sphereParams, 'radius').onChange(updateParameters);
	function updateParameters(){
		if (currentObject.geometry.parameters.radius != sphereParams.radius) {
			updateGeometry(currentObject, new THREE.SphereGeometry(sphereParams.radius));
			if (currentObject.position.y < sphereParams.radius){
				posParams.y = 0;
				moveGeometryY();
			}
		}
	}
}


function initCylinderGui(){
	cylinderFolder = elementFolder.addFolder('Geometry Dimensions');
	cylinderFolder.add(cylinderParams, 'radius').onChange(value => updateParameters("radiusTop", value));
	cylinderFolder.add(cylinderParams, 'length').onChange(value => updateParameters("length", value));
	function updateParameters(changedParam, value){
		if (currentObject.geometry.parameters[changedParam] != value){  // don't regenerate to the object if we're just updating the gui
			const newParams = {...currentObject.geometry.parameters};
			newParams[changedParam] = value;
			if (changedParam == "radiusTop"){
				newParams["radiusBottom"] = value;  // they must be the same
			}
			updateGeometry(currentObject,
						new THREE.CylinderGeometry(newParams.radiusTop, newParams.radiusBottom, newParams.length));
			currentObject.geometry.rotateZ(Math.PI/2);
			render();
			// if (changedParam == "height"){
			// 	posParams.y = 0;
			// 	moveGeometryY();
			// }
		}
	}
}


function initObliqueCylinderGui(){
	obliqueCylinderFolder = elementFolder.addFolder('Geometry Dimensions');
	obliqueCylinderFolder.add(obliqueCylinderParams, 'Faces left radius').onChange(value => updateParameters("radiusTop", value));
	obliqueCylinderFolder.add(obliqueCylinderParams, 'Faces right radius').onChange(value => updateParameters("radiusBottom", value));
	obliqueCylinderFolder.add(obliqueCylinderParams, 'length').onChange(value => updateParameters("height", value));
	obliqueCylinderFolder.add(obliqueCylinderParams, 'Faces Left Trans. y').onChange(value => updateParameters("leftTransY", value));
	obliqueCylinderFolder.add(obliqueCylinderParams, 'Faces Left Trans. z').onChange(value => updateParameters("leftTransZ", value));
	obliqueCylinderFolder.add(obliqueCylinderParams, 'Faces Right Trans. y').onChange(value => updateParameters("rightTransY", value));
	obliqueCylinderFolder.add(obliqueCylinderParams, 'Faces Right Trans. z').onChange(value => updateParameters("rightTransZ", value));
	function updateParameters(changedParam, value){
		if (changedParam == "leftTransY" || changedParam == "rightTransY"){
			changedParam = "topSkewX";
			value = obliqueCylinderParams['Faces Right Trans. y']  - obliqueCylinderParams['Faces Left Trans. y'];
		} else if (changedParam == "leftTransZ" || changedParam == "rightTransZ"){
			changedParam = "topSkewZ";
			value = -(obliqueCylinderParams['Faces Right Trans. z']  - obliqueCylinderParams['Faces Left Trans. z']);
		}
		if (currentObject.geometry.parameters[changedParam] != value){  // don't regenerate to the object if we're just updating the gui
			const newParams = {...currentObject.geometry.parameters};
			newParams[changedParam] = value;
			updateGeometry(currentObject,
						new ObliqueCylinderGeometry(newParams.radiusTop, newParams.radiusBottom, newParams.height,
							                        newParams.topSkewX, newParams.topSkewZ));
			currentObject.geometry.rotateZ(Math.PI/2);
			currentObject.geometry.parameters['Faces Left Trans. y'] = obliqueCylinderParams['Faces Left Trans. y']
			currentObject.geometry.parameters['Faces Left Trans. z'] = obliqueCylinderParams['Faces Left Trans. z']
			currentObject.geometry.parameters['Faces Right Trans. y'] = obliqueCylinderParams['Faces Right Trans. y']
			currentObject.geometry.parameters['Faces Right Trans. z'] = obliqueCylinderParams['Faces Right Trans. z']
			render();
			// if (changedParam == "height"){
			// 	posParams.y = 0;
			// 	moveGeometryY();
			// }
		}
	}
}




function initTrapezoidGui(){
	trapezoidFolder = elementFolder.addFolder('Geometry Dimensions');
	trapezoidFolder.add(trapezoidParams, "Faces Left Trans. y").onChange(value => updateParameters("leftTransY", value));
	trapezoidFolder.add(trapezoidParams, "Faces Left Trans. z").onChange(value => updateParameters("leftTransZ", value));
	trapezoidFolder.add(trapezoidParams, "Faces Left Height").onChange(value => updateParameters("leftDimensY", value));
	trapezoidFolder.add(trapezoidParams, "Faces Left Width").onChange(value => updateParameters("leftDimensZ", value));
	trapezoidFolder.add(trapezoidParams, "Faces Right Trans. y").onChange(value => updateParameters("rightTransY", value));
	trapezoidFolder.add(trapezoidParams, "Faces Right Trans. z").onChange(value => updateParameters("rightTransZ", value));
	trapezoidFolder.add(trapezoidParams, "Faces Right Height").onChange(value => updateParameters("rightDimensY", value));
	trapezoidFolder.add(trapezoidParams, "Faces Right Width").onChange(value => updateParameters("rightDimensZ", value));
	trapezoidFolder.add(trapezoidParams, "length").onChange(value => updateParameters("width", value));
	function updateParameters(changedParam, value){
		if (currentObject.geometry.parameters[changedParam] != value){  // don't regenerate to the object if we're just updating the gui
			const newParams = {...currentObject.geometry.parameters};
			newParams[changedParam] = value;
			updateGeometry(currentObject,
				new TrapezoidGeometry(newParams.leftTransY, newParams.leftTransZ, newParams.leftDimensY, newParams.leftDimensZ,
									newParams.rightTransY, newParams.rightTransZ, newParams.rightDimensY, newParams.rightDimensZ,
									newParams.width));
		}
	}
}


function initBeamGui(){
	beamFolder = elementFolder.addFolder('Geometry Dimensions');
	beamFolder.add(beamParams, "length").onChange(value => updateParameters("width", value));
	beamFolder.add(beamParams, "h").onChange(value => updateParameters("h", value));
	beamFolder.add(beamParams, "s").onChange(value => updateParameters("s", value));
	beamFolder.add(beamParams, "t").onChange(value => updateParameters("t", value));
	beamFolder.add(beamParams, "b").onChange(value => updateParameters("b", value));
	function updateParameters(changedParam, value){
		if (currentObject.geometry.parameters[changedParam] != value){  // don't regenerate to the object if we're just updating the gui
			const newParams = {...currentObject.geometry.parameters};
			newParams[changedParam] = value;
			let newGeom;
			if (currentObject.geometry.type == "IBeamGeometry") {
				newGeom = generateBeam("i-beam", newParams.width, newParams.h, newParams.s, newParams.t, newParams.b, posParams.x, posParams.y, posParams.z);
			} else {
				newGeom = generateBeam("c-beam", newParams.width, newParams.h, newParams.s, newParams.t, newParams.b, posParams.x, posParams.y, posParams.z);
			}
			currentObject.geometry.dispose();
			currentObject.geometry = newGeom;
			if (changedParam == "h"){
				posParams.y = 0;
				moveGeometryY();
			}
			render();
		}
	}
}

/* Functions dealing with relationships between elements */

function updateRelationship(value){
	// Check if a relationship is already defined
	const name1 = selectedObjects[0].name;
	const name2 = selectedObjects[1].name;
	let pair;
	if (relationships[[name1, name2]] != undefined){
		pair = [name1, name2];
	} else if (relationships[[name2, name1]] != undefined){
		pair = [name2, name1];
	}

	if (pair != undefined) {
		// If they're already paired then update the relationship (or remove it if 'none' has been selected)
		if (value == 'none'){
			delete relationships[pair];
			selectedObjects[0].relationshipCount--;
			selectedObjects[1].relationshipCount--;
		} else {
			relationships[pair] = value;
		}
	} else {
		// Add the new relationship
		relationships[[name1, name2]] = value;
		selectedObjects[0].relationshipCount++;
		selectedObjects[1].relationshipCount++;
	}
}


function toggleHighlightUnrelated(value){
	if (value == true){
		// Deselect selected objects to avoid confusion
		try {
			resetColour(gui.children[0].children[0].getValue(), selectedObjects[0]);
			selectedObjects[0] = undefined;
		} catch (TypeError) {;}
		try {
			resetColour(gui.children[0].children[0].getValue(), selectedObjects[1]);
			selectedObjects[1] = undefined;
		} catch (TypeError) {;}
		relationFolder.children[3].hide();
		relationFolder.children[4].hide();
		
		// Highlight orphaned elements
		for (let el of cElements){
			if (el.relationshipCount == 0){
				el.material.color.setHex(otherColours['Orphans']);
			}
		}
	} else {
		resetColours(gui.children[0].children[0].getValue());
	}
	render();
}


function currentRelationship(name1, name2){
	if (relationships[[name1, name2]] != undefined){
		return relationships[[name1, name2]];
	} else if (relationships[[name2, name1]] != undefined){
		return relationships[[name2, name1]];
	}
	return 'none';
}


function toggleHideConnected(value){
	if (value == true){
		for (let el of cElements){
			if (el.relationshipCount > 0){
				el.visible = false;
			}
		}
	} else {
		for (let el of cElements){
			el.visible = true;
		}
	}
	render();
}


function render() {
	renderer.render( scene, camera );
}


export {buildModel};