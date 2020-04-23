let time = 60;
let lockBoard = false;
let score = 0;

$input = $("#input");
$board = $("main");
$alert = $(".alert");

(function setTimmer() {
  const interval = setInterval(() => {
    time--;
    $(".timmer").text(`${time} seconds`);
    if (time === 0) {
      lockBoard = true;
      $(".alert").hide();
      $("#reset").toggleClass("hidden");
      setHighScore(score);
      clearInterval(interval);
    }
  }, 1000);
})();

$(".score").text(`Score: 0`);

$("body").on("submit", "#form", async (evt) => {
  evt.preventDefault();
  if (lockBoard) return;
  input = $input.val();
  if (!input) return;
  response = await checkWord(input);

  displayResult(response, input);

  $input.val("");
});

$("#reset").on("click", () => location.reload());

async function checkWord(input) {
  const response = await axios.get("/check-word", { params: { word: input } });
  return response.data.result;
}

const displayResult = (response, input) => {
  if (response === "ok") {
    $alert.text("Word was found");
    $alert.removeClass("alert-danger");
    $alert.addClass("alert-success");
    score += input.length;
    $(".score").text(`Score: ${score}`);
  } else {
    $alert.text("Word was not found or already found");
    $alert.removeClass("alert-success");
    $alert.addClass("alert-danger");
  }
};

async function setHighScore(score) {
  await axios.post("/end-game", { "high-score": score });
}
