import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 ); 
//field of view, aspect ratio, near clipping plane, far clipping plane

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

fetch('reference4.json')
    .then(response => response.json())
    .then(data => { 
        const word = "about";

        function drawPoint(x, y, z){
            const pointRadius = 0.25;
            const geometry = new THREE.SphereGeometry( pointRadius, 32, 16 );
            const material = new THREE.MeshBasicMaterial( { color: 0xffff00 } );
            const sphere = new THREE.Mesh( geometry, material ); scene.add(sphere);
            sphere.position.x = x;
            sphere.position.y = y;
            sphere.position.z = z;
        }

        function drawLine(x1, y1, z1, x2, y2, z2){
            const points = [];
            points.push (new THREE.Vector3(x1, y1, z1));
            points.push (new THREE.Vector3(x2, y2, z2));
            const geometry = new THREE.BufferGeometry().setFromPoints( points );
            const material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
            const line = new THREE.Line( geometry, material );
            scene.add(line);
        }
        
        var frameidx = 0;
        function render() {
            requestAnimationFrame(render);
            //console.log(frameidx)
            data[word][frameidx]['Left Hand Coordinates'].forEach(function(joint) { //drawing is upside down
                drawPoint(joint['Coordinates'][0]*50, joint['Coordinates'][1]*50*-1, joint['Coordinates'][2]*50);
            })
            data[word][frameidx]['Right Hand Coordinates'].forEach(function(joint) {
                drawPoint(joint['Coordinates'][0]*50, joint['Coordinates'][1]*50*-1, joint['Coordinates'][2]*50);
            })
            renderer.render(scene, camera);
            scene.remove.apply(scene, scene.children);
            frameidx++;
            if(frameidx >= data[word].length){
                frameidx = 0;
            }
        }
        
        render();
    })

camera.position.x = 25;
camera.position.y = -35;
camera.position.z = 25;