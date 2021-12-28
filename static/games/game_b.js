var mat = [[110, 440, 330], [550, 220, 660], [880, 770, 990]];

    //shuffling code

    var lim = 3;
    let origin = 1;
    let size = 100
    function createBoard() {
        let boardb = document.getElementById("boardb");
        for (let i = 0; i < lim; i++) {
            for (let j = 0; j < lim; j++) {
                var tile = document.createElement("img");
                // tile.textContent=mat[i][j]+"";
                tile.setAttribute("alt", mat[i][j]);
                tile.setAttribute("src", "./gameimgs/build/" + mat[i][j] + ".png");
                tile.setAttribute("class", "tiles");
                tile.addEventListener("click", move);
                tile.setAttribute("id", "" + mat[i][j]);
                let tLeft = (j * size) + origin;
                let tTop = (i * size) + origin;
                tile.style.left = tLeft + "px";
                tile.style.top = tTop + "px";
                boardb.appendChild(tile);
            }
        }
    }
    createBoard();
    var countb = 0;
    var solution = [[110, 990, 880], [770, 660, 550], [440, 330, 220]];
    var tempi = 0, tempj = 0;
    var moves = 0;
    function move() {
        countb++;
        var id = this.id;
        let matchFound = false;
        console.log("move is called" + id);
        // var element=document.getElementById(id);
        // element.style.backgroundColor="blanchedalmond";
        for (let i = 0; i < lim; i++) {
            for (let j = 0; j < lim; j++) {
                if (id == mat[i][j]) {
                    var bd = 0, br = 0, bl = 0, bt = 0;
                    let flag = "";
                    // console.log(mat[i][j]);
                    try {
                        bd = mat[i + 1][j];
                    } catch (e) {
                        flag += "d";
                        bd = -1;
                    }
                    try {
                        bt = mat[i - 1][j];
                    } catch (e) {
                        flag += "t";
                        bt = -1;
                    }
                    try {
                        bl = mat[i][j - 1];
                        if (bl == undefined) {
                            bl = -1;
                            flag += "l";
                        }
                    } catch (e) {
                        flag += "l";
                        bl = -1;
                    }
                    try {
                        br = mat[i][j + 1];
                        if (br == undefined) {
                            br = -1;
                            flag += "r";
                        }
                    } catch (e) {
                        flag += "r";
                        br = -1;
                    }
                    console.log(flag + " neighbours  top : " + bt + " bottom : " + bd + " left : " + bl + " right : " + br);
                    // let movable=false;
                    if (countb == 2) {
                        moves++;
                        let text = "moves : " + moves;
                        document.getElementById("gmove").textContent = text;
                        countb = 0;
                        if (tempi == i) {
                            if (Math.abs(tempj - j) == 1) {
                                let tempLeft = (tempj * size) + origin;
                                let nTempLeft = (j * size) + origin;
                                console.log(tempLeft + " " + nTempLeft);
                                document.getElementById(mat[i][j]).style.left = tempLeft + "px";
                                document.getElementById(mat[tempi][tempj]).style.left = nTempLeft + "px";

                                console.log("is neighbour (same row)");
                                let tem = mat[i][j];
                                mat[i][j] = mat[tempi][tempj];
                                mat[tempi][tempj] = tem;
                            }
                            else {
                                console.log("not neighbour");
                            }
                        }
                        else if (tempj == j) {
                            if (Math.abs(tempi - i) == 1) {
                                let tempTop = (tempi * size) + origin;
                                let nTempTop = (i * size) + origin;
                                console.log(tempTop + " " + nTempTop);
                                document.getElementById(mat[i][j]).style.top = tempTop + "px";
                                document.getElementById(mat[tempi][tempj]).style.top = nTempTop + "px";

                                console.log("is neighbour (same col)");

                                let tem = mat[i][j];
                                mat[i][j] = mat[tempi][tempj];
                                mat[tempi][tempj] = tem;
                            }
                            else {
                                console.log("not neighbour");
                            }
                        }
                        else {
                            console.log("not neighbour");
                        }
                    }
                    else if (countb == 1) {
                        tempi = i;
                        tempj = j;
                    }
                    matchFound = true;
                    break;
                }
            }
            if (matchFound) {
                break;
            }
        }
        // console.log(mat); 
        let solutionFound = true;
        for (let i = 0; i < lim; i++) {
            for (let j = 0; j < lim; j++) {
                if (mat[i][j] != solution[i][j]) {
                    solutionFound = false;
                    break;
                }
            }
            if (!solutionFound) {
                break;
            }
        }
        if (solutionFound) {
            alert("congrats !");
            let text = "Congratulations! Game completed in " + moves + " moves";
            document.getElementById("gmove").textContent = text;
            setTimeout(refresh, 3000);
            moves = 0;
        }
    }

