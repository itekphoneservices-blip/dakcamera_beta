const res = await fetch("http://127.0.0.1:8000/apply", {
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: JSON.stringify(data)
});
