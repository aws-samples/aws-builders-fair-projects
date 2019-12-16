export const PuenteAdapter = {
    classify: (imgString) => {
        return fetch("<< update with your own API url - found on dashboard of API gateway>>", {
            crossDomain: true,
            method: "POST",
            body: JSON.stringify({
              image: imgString
            }),
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json"
            }
          })
            .then(res => {
              return res.json();
            })
    }
}