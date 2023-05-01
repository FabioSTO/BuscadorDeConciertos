const valor = document.querySelector("#valor")
  const presupuesto = document.querySelector("#presupuesto")

  valor.textContent = presupuesto.value

  presupuesto.addEventListener("input", (event) => {
    valor.textContent = event.target.value
  })
