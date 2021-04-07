class BoggleGame {
    constructor(boardId, seconds = 60) {
        this.secs = seconds;
        this.showTimer();

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        //setInterval function allows clocklogic to run every second
        this.clock = setInterval(this.clockLogic.bind(this), 1000);

        $(".add-guess", this.board).on("submit", this.handleSubmit.bind(this));
    }
    
    async clockLogic() {
        this.secs = this.secs - 1;
        this.showTimer();

        if (this.secs < 0) {
            //when the timer gets past zero end the game
            clearInterval(this.clock);
            await this.scoreGame();
        }
    }

    showTimer() {
        $("#clock", this.board).text(this.secs);
    }
    
    displayMessage(txt, cls) {
        $("#message").text(txt).removeClass().addClass(`${cls}`);
    }

    async handleSubmit(evt) {
        evt.preventDefault();

        const $word = $(".guessInput", this.board);
    
        let word = $word.val();
        if (!word) {
            return;
        }
        
        if (this.words.has(word)) {
            this.displayMessage(`${word} has already been found`, "err")
            return;
        }

        const resp = await axios.get("/check-word", { params: { word: word}});
        
        if (resp.data.result === "not-word") {
            this.displayMessage(`${word} cannot be found in the dictionary`, "err");
        } else if (resp.data.result === "not-on-board") {
            this.displayMessage(`${word} cannot be found on the board`, "err");
        } else {
            $(".words", this.board).append($("<li>", { text: word }));
            this.score += word.length;
            this.displayMessage();
            this.words.add(word);
            this.displayMessage(`Added: ${word}`, "ok");
        }

        $word.val("").focus();
    }

    async scoreGame() {
        $(".add-word", this.board).hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
            this.displayMessage(`You set a new record!: ${this.score}`, "ok");
        } else {
            this.displayMessage(`Your final score is: ${this.score}`, "ok");
        }
    }
}