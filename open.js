
var result = []
function getMotivation(trueId) {
    (async () =>{
        const request = await fetch("https://private.proverki.gov.ru/erknm-catalogs/api/knm/"+trueId, {
          "headers": {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
          },
          "referrer": "https://private.proverki.gov.ru/",
          "referrerPolicy": "origin",
          "body": null,
          "method": "GET",
          "mode": "cors",
          "credentials": "include"
        });
        const response = await request.json();
        result.push(response)
    })();
}


var knms = []   // Сюда номера проверок
var contents = []
function getFullKNM(trueId) {
    (async () =>{
        const req = await fetch("https://private.proverki.gov.ru/erknm-catalogs/api/knm/" + trueId, {
          "headers": {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
          },
          "referrer": "https://private.proverki.gov.ru/",
          "referrerPolicy": "origin",
          "body": null,
          "method": "GET",
          "mode": "cors",
          "credentials": "include"
        });const res = await req.json();contents.push([trueId, res['knmErknm']['approve']['rejectReasonNote']])
    })();
}
knms.forEach(n => getFullKNM(n));
