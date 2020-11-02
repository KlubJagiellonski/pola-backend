import React from 'react'

const SearchModal = ({data}) => {
    return (
        <div>
            <h2>
                {data.name}
            </h2>
            {data.name !== "Nieprawidłowy kod" &&
            <>
                <div data-testid="pl-score">
                    {data.plScore} pkt
                </div>
                <div>
                    udział polskiego kapitału {data.plCapital} %
                </div>
                <div>
                    <input data-testid="pl-workers" type='checkbox' disabled
                           checked={data.plWorkers === 100}/>
                    produkuje w Polsce
                </div>
                <div>
                    <input data-testid="pl-rnd" type='checkbox' disabled
                           checked={data.plRnD === 100}/>
                    prowadzi badania i rozwój w Polsce
                </div>
                <div>
                    <input data-testid="pl-registered" type='checkbox' disabled
                           checked={data.plRegistered === 100}/>
                    zajerestrowana w Polsce
                </div>
                <div>
                    <input data-testid="pl-not-glob-ent" type='checkbox' disabled
                           checked={data.plNotGlobEnt === 100}/>
                    nie jest częścią zagranicznego koncernu
                </div>
                {data.is_friend && (
                    <div>
                        To jest przyjaciel Poli
                    </div>
                )}
                <div>
                    {data.description}
                </div>
            </>
            }
        </div>
    )
}

export default SearchModal