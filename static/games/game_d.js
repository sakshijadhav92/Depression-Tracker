console.log("Let's begin ");

    var data = [
        {
            "id": 1222,
            "path": "./gameimgs/jigsaw/nature/1.jpg"
        },
        {
            "id": 2222,
            "path": "./gameimgs/jigsaw/nature/2.jpg"
        },
        {
            "id": 3222,
            "path": "./gameimgs/jigsaw/nature/3.jpg"
        },
        {
            "id": 4222,
            "path": "./gameimgs/jigsaw/nature/4.jpg"
        },

        {
            "id": 5222,
            "path": "./gameimgs/jigsaw/nature/5.jpg"
        },
        {
            "id": 6222,
            "path": "./gameimgs/jigsaw/nature/6.jpg"
        },
        {
            "id": 7222,
            "path": "./gameimgs/jigsaw/nature/7.jpg"
        },
        {
            "id": 8222,
            "path": "./gameimgs/jigsaw/nature/8.jpg"
        },


        {
            "id": 9222,
            "path": "./gameimgs/jigsaw/nature/9.jpg"
        },


    ]

    var curr = 0;
    var pagex = 0;
    var pagey = 0;
    var elem = null;
    var jdivct = 0;
    var table = document.getElementById("jtab");
    var collection = document.getElementById("jcards");
    var solution = [9, 8, 7, 6, 5, 4, 3, 2, 1]

    function shuffle(array) {
        let currentIndex = array.length, randomIndex;

        // While there remain elements to shuffle...
        while (currentIndex != 0) {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;

            // And swap it with the current element.
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex], array[currentIndex]];
        }

        return array;
    }
    data = shuffle(data);



    window.addEventListener("mousemove", (e) => {
        pagex = e.pageX;
        pagey = e.pageY;
        if (elem != null) {
            elem.style.left = (5 + pagex) + "px";
            elem.style.top = (pagey - 40) + "px";
        }
    });

    function gameInit() {
        for (let i = 0; i < table.rows.length; i++) {
            for (let j = 0; j < table.rows[i].cells.length; j++) {
                // console.log(""+table.rows[i].cells[j].id+" ");
                document.getElementById(table.rows[i].cells[j].id).addEventListener("click", (e) => {
                    // console.log("click event is running "+curr);
                    // console.log(document.getElementById(curr))
                    // console.log(e.target.parentNode.nodeName);
                    if (elem != null) {
                        elem.className = "jcard";
                        elem = null;
                        try {
                            e.target.append(document.getElementById(curr));
                            jdivct=0;
                            if (isCorrect()) {
                                console.log("okay well done");
                            }
                        } catch (e) {
                            console.log("Just working ")
                        }
                    } else {

                    }
                    // elem.removeEventListener("click");
                })

            }
        }


        for (let i = 0; i < data.length; i++) {
            // for(let j=0;j<table.rows[i].cells.length;j++){
            //     // console.log(""+table.rows[i].cells[j].id+" ");
            //     document.getElementById(table.rows[i].cells[j].id).addEventListener("touch")
            // }
            let jcard = document.createElement("img");
            jcard.setAttribute("class", "jcard");
            jcard.setAttribute("id", data[i].id);
            jcard.setAttribute("src", data[i].path);
            jcard.addEventListener("click", (e) => {
                // console.log("image clicked "+e.target.id);  
                curr = e.target.id;
                if (e.target.parentNode.nodeName == "DIV") {
                    console.log(e.target.parentNode.nodeName+" is clicked")
                    if(jdivct>=2){
                        console.log("another card is clicked ");
                        e.target.className= "jcard";
                        jdivct=0;
                        curr=0;
                        elem=null;
                    }else{
                        e.target.className += " jmove";
                        elem = e.target;
                    }

                } else if (e.target.parentNode.nodeName == "TD") {
                    collection.append(document.getElementById(curr))
                }
                

            });


            jcard.addEventListener("drop", (e) => {
                // collection.append(document.getElementById(curr))
                curr = 0
                e.preventDefault();
                // console.log("")
            });
            collection.append(jcard);

        }

        collection.addEventListener("click", () => {
            jdivct++;
            if (jdivct >=2) {
                console.log("keep the card");
                jdivct = 0;
                document.getElementById(curr).classList.toggle("jmove");
                curr=0;
                elem=null;
		    }
        });
    }
    gameInit();
    function isCorrect() {
        let flag = true;
        let tableComplete = true;
        for (let i = 0; i < table.rows.length; i++) {
            for (let j = 0; j < table.rows[i].cells.length; j++) {
                console.log();
                if (table.rows[i].cells[j].firstChild == null) {
                    flag = false;
                    tableComplete = false;
                    break;
                }
            }
            if (!flag) {
                break;
            }
        }

        if (flag) {

            let count = -1;
            for (let i = 0; i < table.rows.length; i++) {
                for (let j = 0; j < table.rows[i].cells.length; j++) {
                    // console.log();
                    // console.log(table.rows[i].cells[j].firstChild.id)
                    if (table.rows[i].cells[j].firstChild.id != solution[++count]) {
                        flag = false;
                        break;
                    }
                }
                if (!flag) {
                    break;
                }
            }
        }
        if (flag) {
            alert("well done")
            document.getElementById("say").textContent = "Congratulations you win!"
        }
        if (tableComplete && !flag) {
            alert("oops try again");
        }

        return flag;
    }
    isCorrect()

    function reset() {
        elem = null;
        curr = 0;
        window.location.reload();
    }