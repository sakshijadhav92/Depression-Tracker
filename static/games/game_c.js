var imageArray = [
    {
        imgname: "exp1",
        imgSrc: "./gameimgs/whakaboom/exp1.png"
    },
    {
        imgname: "exp2",
        imgSrc: "./gameimgs/whakaboom/exp2.png"
    },
    {
        imgname: "exp3",
        imgSrc: "./gameimgs/whakaboom/exp3.png"
    },
    {
        imgname: "exp4",
        imgSrc: "./gameimgs/whakaboom/exp4.png"
    },
    {
        imgname: "exp5",
        imgSrc: "./gameimgs/whakaboom/exp5.png"
    },
    {
        imgname: "exp6",
        imgSrc: "./gameimgs/whakaboom/exp6.png"
    },
    {
        imgname: "exp7",
        imgSrc: "./gameimgs/whakaboom/exp7.png"
    },
    {
        imgname: "exp8",
        imgSrc: "./gameimgs/whakaboom/exp8.png"
    }
];


var gscore = 0;
var ghits = 0;

//mousehover event 

//appering baddies
var gboard = document.getElementById("gboard");
// window.onload=()=>{
document.getElementById("startWhacking").addEventListener("click", startWhacking);
document.getElementById("stopWhacking").addEventListener("click", stopWhacking);

// }
function creategBoard() {
    console.log("I am called")
    for (let i = 0; i < 16; i++) {
        let gimage = document.createElement("img");
        gimage.setAttribute("id", i + 1000);
        gimage.setAttribute("src", "./gameimgs/whakaboom/blank.png")
        // image.setAttribute("onclick", "bang('"+i+"')")
        gimage.addEventListener("click", bang);
        gimage.setAttribute("width", "100");
        gimage.setAttribute("height", "100");
        gboard.append(gimage);
    }
}

creategBoard();
var tioutFunc = "";
function startWhacking() {
    tioutFunc = setInterval(function () {
        var randomId = Math.floor(Math.random() * 16) + 1000;
        let gcard = document.getElementById(randomId);
        var randomIndex = Math.floor(Math.random() * 5);

        gcard.setAttribute("src", imageArray[randomIndex].imgSrc);
        setTimeout(function () {
            hideCard(randomId);
        }, 1000);
    }, 900);
}
function stopWhacking() {
    window.location.reload();
}


function hideCard(id) {
    document.getElementById(id).setAttribute("src", "./gameimgs/whakaboom/blank.png");
}

function bang() {
    let id = this.id;
    let gcard = document.getElementById(id);
    let cardImg = gcard.getAttribute("src");
    if (cardImg != "./gameimgs/whakaboom/blank.png") {
        ghits++;
        gscore += 15;
        document.getElementById("ghits").textContent = ghits;
        document.getElementById("sc").textContent = gscore;
        gcard.setAttribute("src", "./gameimgs/whakaboom/bang.png")
    }
}