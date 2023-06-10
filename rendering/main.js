import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 ); //params: field of view, aspect ratio, near clipping plane, far clipping plane

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

fetch('reference4.json')
    .then(response => response.json())
    .then(data => { 
        const word = "smoke";

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

        function redistributeElements(left, right) { //fixes the problem where more than 21 are identified as left and lets the lines be drawn properly 
            if (left.length > 21) {
                const redistributedElements = left.splice(21);
                right.push(...redistributedElements);
            } else if (right.length > 21) {
                const redistributedElements = right.splice(21);
                left.push(...redistributedElements);
            }
        }

        function connectLines(frameidx){
            const edgeList = [[0,1],[1,2], [2,3], [3,4], [0,5], [5,6], [6,7], [7,8], [5,9], [9,10], [10,11], [11,12], [9,13], [13,14], [14,15], [15,16], [13,17], [17,18], [18,19], [19,20], [0,17]];
            var left = data[word][frameidx]['Left Hand Coordinates'];
            var right = data[word][frameidx]['Right Hand Coordinates'];

            redistributeElements(left, right);
            
            edgeList.forEach(function(edge){
                const u = edge[0];
                const v = edge[1];
                if (left[u] && left[v]){
                    const l1 = left[u]['Coordinates'];
                    const l2 = left[v]['Coordinates'];
                    drawLine(l1[0]*50, l1[1]*-50, l1[2]*50, l2[0]*50, l2[1]*-50, l2[2]*50);
                }
                if (right[u] && right[v]){
                    const r1 = right[u]['Coordinates'];
                    const r2 = right[v]['Coordinates'];
                    drawLine(r1[0]*50, r1[1]*-50, r1[2]*50, r2[0]*50, r2[1]*-50, r2[2]*50);
                }
            })
        } 

        var frameidx = 0;
        function render() {
            requestAnimationFrame(render);
            //console.log(frameidx)

            data[word][frameidx]['Left Hand Coordinates'].forEach(function(joint) { 
                drawPoint(joint['Coordinates'][0]*50, joint['Coordinates'][1]*-50, joint['Coordinates'][2]*50);
            })
            data[word][frameidx]['Right Hand Coordinates'].forEach(function(joint) {
                drawPoint(joint['Coordinates'][0]*50, joint['Coordinates'][1]*-50, joint['Coordinates'][2]*50);
            })

            connectLines(frameidx);

            renderer.render(scene, camera);
            scene.remove.apply(scene, scene.children);

            frameidx++;
            if(frameidx >= data[word].length){
                frameidx = 0;
            }
        }
        
        render();
    })

camera.position.set(25, -35, 25);
