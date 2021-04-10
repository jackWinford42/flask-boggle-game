class BoggleGame {
    constructor(boardId) {
        this.board = $("#" + boardId);
        this.secs = 60;
        this.showTimer();
        this.score = 0;
        this.answers = new Set();

        //setInterval function allows clocklogic to run every second
        this.clock = setInterval(this.clockLogic.bind(this), 1000);

        $(".add-guess", this.board).on("submit", this.serveWord.bind(this));
    }
    
    async clockLogic() {
        this.secs = this.secs - 1;
        this.showTimer();
        
        if (this.secs < 1) {
            //when the timer gets past zero end the game
            clearInterval(this.clock);

            await this.scoreGame();
        }
    }

    showTimer() {
        if (this.secs < 10) {
            $("#clock", this.board).text("0" + this.secs);
        } else {
            $("#clock", this.board).text(this.secs);
        }
    }
    
    displayMessage(txt, cls) {
        $("#message").text(txt)

        $("#message").removeClass()

        $("#message").addClass(`${cls}`);
    }

    serveWord(e) {
        e.preventDefault();

        const answer = $(".guessInput", this.board).val();

        $(".guessInput", this.board).val("").focus();

        //do nothing if answer is blank
        if (answer === "") {
            return;
        }

        //if answer has been guessed previously
        if (this.answers.has(answer)) {
            this.displayMessage(`${word} has already been found`, "error");
            return;
        }

        this.verifyAnswer(answer);
    }

    async verifyAnswer(answer) {

        const response = await axios.get("/verify-guess", { params: { word: answer}});

        if (response.data.result === "not-on-board" || response.data.result === "not-word") {

            this.displayMessage(`${answer} is invalid (either not a word or on the board) guess again`, "error");
        } else {

            $(".answers", this.board).append($("<li>", { text: answer }));
            this.score += answer.length;
            $(".score", this.board).text(this.score);
            this.answers.add(answer);
            this.displayMessage(`Successfully listed and scored: ${answer}`, "ok");
        }

        
    }

    async scoreGame() {
        $(".add-guess", this.board).hide();
        const resp = await axios.post("/score-game", { score: this.score });

        if (resp.data.brokeRecord) {
            this.displayMessage(`You set a new record!: ${this.score}`, "ok");
        } else {
            this.displayMessage(`Your final score is: ${this.score}`, "ok");
        }
    }
}