document.addEventListener("DOMContentLoaded", function () {
  const powerBtn = document.getElementById("power-btn");
  const alturaCorte = document.getElementById("altura-corte");
  const velocidadeValor = document.getElementById("velocidade-valor");
  const btnAumentar = document.getElementById("aumentar-velocidade");
  const btnDiminuir = document.getElementById("diminuir-velocidade");
  const btnMostrarMapa = document.getElementById("mostrar-mapa"); // Adicionando o botão do mapa

  let ligado = false;
  let velocidade = 90; // Valor inicial da velocidade

  // Pegando a URL da API do atributo do body
  const API_URL = 'http://127.0.0.1:5001';

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
      .then(data => {
        console.log("Resposta da API:", data);
      })
      .catch(error => console.error("Erro ao ajustar altura:", error));
  });


  btnAumentar.addEventListener("click", function () {
    fetch(`${API_URL}/speed-up`, { method: "GET" })
        .then(response => response.json())
        .then(data => {
            if (data.status && data.status.velocidade !== undefined) {
                velocidade = data.status.velocidade;
                velocidadeValor.textContent = velocidade; // Atualize o valor no frontend
            }
        })
        .catch(error => console.error("Erro ao aumentar velocidade:", error));
  });

  btnDiminuir.addEventListener("click", function () {
      fetch(`${API_URL}/speed-down`, { method: "GET" })
          .then(response => response.json())
          .then(data => {
              if (data.status && data.status.velocidade !== undefined) {
                  velocidade = data.status.velocidade;
                  velocidadeValor.textContent = velocidade; // Atualize o valor no frontend
              }
          })
          .catch(error => console.error("Erro ao reduzir velocidade:", error));
  });

  

  if (btnMostrarMapa) {
    btnMostrarMapa.addEventListener("click", function () {
      fetch(`${API_URL}/map`, { method: "GET" })
        .then(response => response.json())
        .then(data => console.log("Mapa carregado:", data))
        .catch(error => console.error("Erro ao carregar mapa:", error));
    });
  }

});
