document.addEventListener("DOMContentLoaded", function () {
    const powerBtn = document.getElementById("power-btn");
    const alturaCorte = document.getElementById("altura-corte");
    const velocidade = document.getElementById("velocidade");
    const velocidadeValor = document.getElementById("velocidade-valor");

    let ligado = false;

    // Pegando a URL da API do atributo do body
    const API_URL = document.body.getAttribute("data-api-url");

    powerBtn.addEventListener("click", function () {
        ligado = !ligado;
        powerBtn.textContent = ligado ? "Desligar" : "Ligar";
        powerBtn.classList.toggle("off", ligado);

        fetch(`${API_URL}/ligar`, {
            method: "POST",
            body: JSON.stringify({ ligado }),
            headers: { "Content-Type": "application/json" }
        }).then(response => response.json())
          .then(data => console.log("Resposta da API:", data))
          .catch(error => console.error("Erro ao ligar/desligar:", error));
    });

    alturaCorte.addEventListener("change", function () {
        fetch(`${API_URL}/altura_corte`, {
            method: "POST",
            body: JSON.stringify({ altura: alturaCorte.value }),
            headers: { "Content-Type": "application/json" }
        }).then(response => response.json())
          .then(data => console.log("Resposta da API:", data))
          .catch(error => console.error("Erro ao ajustar altura:", error));
    });

    velocidade.addEventListener("input", function () {
        velocidadeValor.textContent = velocidade.value;

        fetch(`${API_URL}/velocidade`, {
            method: "POST",
            body: JSON.stringify({ velocidade: parseInt(velocidade.value) }),
            headers: { "Content-Type": "application/json" }
        }).then(response => response.json())
          .then(data => console.log("Resposta da API:", data))
          .catch(error => console.error("Erro ao ajustar velocidade:", error));
    });
});
