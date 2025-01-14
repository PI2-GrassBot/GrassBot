document.addEventListener("DOMContentLoaded", () => {
    const apiUrl = document.body.dataset.apiUrl;
  
    const powerBtn = document.getElementById("power-btn");
    const alturaSelect = document.getElementById("altura-corte");
    const velocidadeRange = document.getElementById("velocidade");
    const velocidadeValor = document.getElementById("velocidade-valor");
  
    // Atualizar visualização da velocidade
    velocidadeRange.addEventListener("input", () => {
      velocidadeValor.textContent = velocidadeRange.value;
    });
  
    // Ligar/desligar o cortador
    powerBtn.addEventListener("click", async () => {
      const ligado = powerBtn.textContent === "Ligar";
      try {
        const response = await fetch(`${apiUrl}/power`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ligado }),
        });
        if (response.ok) {
          powerBtn.textContent = ligado ? "Desligar" : "Ligar";
        } else {
          alert("Erro ao alterar o estado do cortador.");
        }
      } catch (error) {
        console.error("Erro ao conectar à API:", error);
      }
    });
  
    // Alterar altura do corte
    alturaSelect.addEventListener("change", async () => {
      try {
        const response = await fetch(`${apiUrl}/altura_corte`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ altura: alturaSelect.value }),
        });
        if (!response.ok) {
          alert("Erro ao alterar a altura do corte.");
        }
      } catch (error) {
        console.error("Erro ao conectar à API:", error);
      }
    });
  
    // Alterar velocidade
    velocidadeRange.addEventListener("change", async () => {
      try {
        const response = await fetch(`${apiUrl}/velocidade`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ velocidade: parseInt(velocidadeRange.value, 10) }),
        });
        if (!response.ok) {
          alert("Erro ao alterar a velocidade.");
        }
      } catch (error) {
        console.error("Erro ao conectar à API:", error);
      }
    });
  });
  