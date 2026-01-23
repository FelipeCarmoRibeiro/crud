async function createUserAndGame() {
    // cria usuário
    const resUser = await fetch("/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: name.value,
            email: email.value,
            password: password.value
        })
    });

    const user = await resUser.json();

    // cria jogo usando o ID do usuário
    await fetch("/games", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: title.value,
            price: price.value,
            owner: user.id
        })
    });

    loadUsers();
    loadGames();
}

