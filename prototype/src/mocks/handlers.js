import {rest} from 'msw'

export const prepareGetCodeMock = ({code, name, description, pl_score, pl_capital, pl_workers, pl_rnd, pl_registered, pl_not_glob_ent} = {}) => {

    let result = {
        product_id: 21156,
        code: code || "5900334005526",
        name: name || "TEST-PRODUCT",
        card_type: "type_white",
        plScore: pl_score == null ? 100 : pl_score,
        altText: null,
        plCapital: pl_capital == null ? 100 : pl_capital,
        plCapital_notes: "",
        plWorkers: pl_workers == null ? 100 : pl_workers,
        plWorkers_notes: "",
        plRnD: pl_rnd == null ? 100 : pl_rnd,
        plRnD_notes: "",
        plRegistered: pl_registered == null ? 100 : pl_registered,
        plRegistered_notes: "",
        plNotGlobEnt: pl_not_glob_ent == null ? 100 : pl_not_glob_ent,
        plNotGlobEnt_notes: "",
        report_text: "Zg\u0142o\u015b je\u015bli posiadasz bardziej aktualne dane na temat tego produktu",
        report_button_text: "Zg\u0142o\u015b",
        report_button_type: "type_white",
        is_friend: false,
        description: description || "TEST-DESCRIPTION",
        sources: {
            "Dane z KRS": "http://mojepanstwo.pl/dane/krs_podmioty/498181",
            "Strona producenta": "https://tymbark.com/o-firmie/o-firmie/o-firmie/"
        },
        donate: {
            show_button: true,
            url: "https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/",
            title: "Wspieraj aplikacj\u0119 Pola"
        }
    }

    if (code != null) {
        if (code.startsWith('977') || code.startsWith('978') || code.startsWith('979')) {
            result['name'] = 'Kod ISBN/ISSN/ISMN'
            result['altText'] = `
                Zeskanowany kod jest kodem
                ISBN/ISSN/ISMN dotyczącym książki,
                czasopisma lub albumu muzycznego.
                Wydawnictwa tego typu nie są aktualnie
                w obszarze zainteresowań Poli.
            `
            result['report_text'] = "To nie jest książka, czasopismo lub album muzyczny? Prosimy o zgłoszenie"
        } else if (code.startsWith('40')) {
            // Niemcy
            result['plScore'] = 0
            result['card_type'] = 'grey'
            result['name'] = 'Miejsce rejestracji: Nimecy'
            result['altText'] = `
                Ten produkt został wyprodukowany
                przez zagraniczną firmę, której
                miejscem rejestracji jest: Niemcy.
                `
        }
    }

    return result;
}


export const handlers = [
    rest.get('/a/v3/get_by_code',
        (req, res, ctx) => {
            const code = req.url.searchParams.get('code')

            let mock_data = prepareGetCodeMock({code})

            return res(
                ctx.status(200),
                ctx.json(mock_data)
            )
        }
    ),
]
