document.getElementById("form").onsubmit = async e => {
  e.preventDefault();
  const data = {budget: +document.getElementById("budget").value, days: +document.getElementById("days").value, interests: document.getElementById("interests").value.split(","), departure: document.getElementById("departure").value};
  try {
   const res = await fetch("https://flight-ai-lab.onrender.com/api/search", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(data)});
    const json = await res.json();
    const f = json.best_flight;
    document.getElementById("result").style.display="block";
    document.getElementById("result").innerHTML = `<b>✈️ ${f.airline}</b><br>Куда: ${f.destination}<br>Цена: ${f.price} ₽ | Длительность: ${f.duration} ч | Пересадки: ${f.stops}<br><i>Скор ИИ: ${json.score}</i>`;
  } catch(err) { alert("Ошибка подключения к API. Запусти сервер!"); }
};