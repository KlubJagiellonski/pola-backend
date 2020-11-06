import React from 'react'
import { Wrapper, BigSection, SmallSection, Section } from './SearchModal.css'
import ModalTitle from './../../components/ModalTitle'
import ModalProgressiveBar from './../../components/ModalProgressiveBar'
import ModalCheckbox from './../../components/ModalCheckbox'

const SearchModal = ({ data, close }) => {

    return (
        <Wrapper>
            <ModalTitle
                title={data.name}
                close={close}
            />
            {data.name !== "Nieprawidłowy kod" &&
                <>
                    <BigSection>
                        <ModalProgressiveBar
                            now={data.plScore}
                            suffix={'pkt'}
                            size='big'
                        />
                    </BigSection>
                    <SmallSection>
                        <Section>
                            <p style={{ margin: '0 0 8px 0' }}>udział polskiego kapitału</p>
                            <ModalProgressiveBar
                                now={data.plCapital}
                                suffix={'%'}
                                size='small'
                            />
                        </Section>
                        <div style={{marginTop: 20}}>
                            <Section>
                                <ModalCheckbox
                                    dataTestId="pl-workers"
                                    value={data.plWorkers}
                                    title="produkuje w Polsce"
                                />
                            </Section>
                            <Section>
                                <ModalCheckbox
                                    dataTestId="pl-rnd"
                                    value={data.plRnD}
                                    title="prowadzi badania i rozwój w Polsce"
                                />
                            </Section>
                            <Section>
                                <ModalCheckbox
                                    dataTestId="pl-registered"
                                    value={data.plRegistered}
                                    title="zajerestrowana w Polsce"
                                />
                            </Section>
                            <Section>
                                <ModalCheckbox
                                    dataTestId="pl-not-glob-ent"
                                    value={data.plNotGlobEnt}
                                    title="nie jest częścią zagranicznego koncernu"
                                />
                            </Section>
                        </div>
                        {/* {data.is_friend && (
                            <Section>
                                To jest przyjaciel Poli
                            </Section>
                        )} */}
                        <Section>
                            {data.description}
                        </Section>
                    </SmallSection>
                </>
            }
        </Wrapper>
    )
}

export default SearchModal