var score = 0, failed = 0;
    const cardsInputArray = [
        {
            cname: 'circle',
            image: './gameimgs/match/circle.png'
        },
        {
            cname: 'thunder',
            image: './gameimgs/match/thunder.png'
        },
        {
            cname: 'red_heart',
            image: './gameimgs/match/red_heart.png'
        },
        {
            cname: 'vertical_rectangle',
            image: './gameimgs/match/vertical_rectangle.png'
        },
        {
            cname: 'red_heart',
            image: './gameimgs/match/red_heart.png'
        },
        {
            cname: 'circle',
            image: './gameimgs/match/circle.png'
        },
        {
            cname: 'down_arrow',
            image: './gameimgs/match/down_arrow.png'
        },

        {
            cname: 'four_point_star',
            image: './gameimgs/match/four_point_star.png'
        },
        {
            cname: 'four_point_star',
            image: './gameimgs/match/four_point_star.png'
        },
        {
            cname: 'vertical_rectangle',
            image: './gameimgs/match/vertical_rectangle.png'
        },
        {
            cname: 'star',
            image: './gameimgs/match/star.png'
        },

        {
            cname: 'hexagon',
            image: './gameimgs/match/hexagon.png'
        },
        {
            cname: 'down_arrow',
            image: './gameimgs/match/down_arrow.png'
        },
        {
            cname: 'star',
            image: './gameimgs/match/star.png'
        },
        {
            cname: 'thunder',
            image: './gameimgs/match/thunder.png'
        },
        {
            cname: 'hexagon',
            image: './gameimgs/match/hexagon.png'
        }
    ];


    function shuffel(elements) {
        for (let i = 0; i < elements.length; i++) {
            let swapVariable = Math.floor(i * Math.random());
            let temp = elements[i];
            elements[i] = elements[swapVariable];
            elements[swapVariable] = temp;
        }
        return elements;
    }

    var cards = [];


    var cardsFlipped = [];
    var cardsFlippedIds = [];

    const board = document.getElementById("board");
    function makeBoard() {
        console.log("creating board");
        cards = shuffel(cardsInputArray);
        for (let i = 0; i < cards.length; i++) {
            var card = document.createElement("img");
            card.setAttribute("src", "./gameimgs/match/general.png");
            card.setAttribute("id", i);
            card.setAttribute("class", "imgc");
            card.addEventListener("click", flipcard);
            board.appendChild(card);
        }
    }
    makeBoard();

    function displayScore() {
        document.getElementById("score").textContent = score;
        document.getElementById("failed").textContent = failed;
        if (score == 8) {
            if (failed <= 10) {
                document.getElementById("comments").textContent = "Congrats ! cards matched Nice memory !";
            }
            let totalAtmps = score + failed;
            alert("Game Won !\n" + "Total Attempts : " + totalAtmps);
            setTimeout(refresh, 3000);
        }
    }
    function refresh() {
        window.location.reload();
    }
    function checkForMatch() {
        var flag = false;
        var grid = document.getElementById("board");
        var temporaryCards = grid.querySelectorAll("img");
        var card1 = cardsFlippedIds[0];
        var card2 = cardsFlippedIds[1];
        if (cardsFlipped[0] === cardsFlipped[1]) {
            document.getElementById("comments").textContent = "Congrats ! cards matched :)";
            temporaryCards[card1].setAttribute("src", "./gameimgs/match/done.png");
            temporaryCards[card2].setAttribute("src", "./gameimgs/match/done.png");
            flag = true;
            score += 1;
        }
        else {
            document.getElementById("comments").textContent = "Try again :(";
            failed += 1;
        }
        if (!flag) {
            temporaryCards[card1].setAttribute("src", "./gameimgs/match/general.png");
            temporaryCards[card2].setAttribute("src", "./gameimgs/match/general.png");
        }
        else {
            temporaryCards[card1].removeEventListener("click", flipcard);
            temporaryCards[card2].removeEventListener("click", flipcard);
        }
        cardsFlippedIds = [];
        cardsFlipped = [];
        displayScore();
    }

    function flipcard() {
        var cardId = this.getAttribute("id");
        cardsFlipped.push(cards[cardId].cname);
        cardsFlippedIds.push(cardId);
        if (cardsFlippedIds[0] == cardsFlippedIds[1]) {
            let cid = cardsFlippedIds[0];
            alert("Same card clicked ");
            document.getElementById(cid).setAttribute("src", "./gameimgs/match/general.png");
            cardsFlipped = [];
            cardsFlippedIds = [];
        }
        else {
            this.setAttribute("src", cards[cardId].image);
            if (cardsFlipped.length == 2) {
                setTimeout(checkForMatch, 500);
            }
        }
    }