import React, { useState } from 'react';
import axios from 'axios';
import { 
  Sparkles, 
  ArrowRight, 
  ArrowLeft, 
  Check, 
  Star, 
  RotateCcw, 
  Heart, 
  ShieldAlert, 
  Droplets, 
  Zap, 
  Smile, 
  Info,
  CheckCircle2
} from 'lucide-react';

// Configuração dinâmica da URL da API (lê do .env / Vercel com fallback local)
const RAW_API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const API_BASE_URL = RAW_API_URL.replace(/\/+$/, '');

export default function App() {
  // Máquina de estados das telas: 'welcome' | 'anamnese' | 'loading' | 'results'
  const [screen, setScreen] = useState('welcome');
  
  // Controle do passo atual no Wizard (1 a 4)
  const [step, setStep] = useState(1);

  // Estado do formulário de anamnese
  const [formData, setFormData] = useState({
    curvatura: 3,        // 2, 3 ou 4
    porosidade: 2,       // 1, 2 ou 3
    dano_quimico: 0,     // 0 ou 1
    ressecamento_opacidade: 0,
    alta_porosidade_quimica: 0,
    frizz_falta_definicao: 1,
    transicao_capilar: 0,
    couro_sensivel_oleoso: 0
  });

  // Resposta da recomendação da API
  const [recommendationResult, setRecommendationResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Estado de feedback pós-atendimento
  const [feedbackSent, setFeedbackSent] = useState({});
  const [feedbackRating, setFeedbackRating] = useState({});

  // Manipuladores de estado do formulário
  const handleSelect = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleToggleQueixa = (field) => {
    setFormData(prev => ({ ...prev, [field]: prev[field] === 1 ? 0 : 1 }));
  };

  // Submissão do formulário para a API FastAPI
  const handleSubmitAnamnese = async () => {
    setScreen('loading');
    setErrorMessage(null);

    // Garante que pelo menos 1 queixa seja marcada
    const totalQueixas = 
      formData.ressecamento_opacidade + 
      formData.alta_porosidade_quimica + 
      formData.frizz_falta_definicao + 
      formData.transicao_capilar + 
      formData.couro_sensivel_oleoso;

    const payload = { ...formData };
    if (totalQueixas === 0) {
      payload.frizz_falta_definicao = 1;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/recommend?top_k=3`, payload);
      setRecommendationResult(response.data);
      setScreen('results');
    } catch (err) {
      console.error("Erro ao chamar API de recomendação:", err);
      setErrorMessage(
        err.response?.data?.detail || 
        "Não foi possível conectar ao motor de recomendação. Verifique se a API FastAPI está ativa na porta 8000."
      );
      setScreen('anamnese');
    }
  };

  // Envio de Feedback interativo
  const handleSendFeedback = async (nomeProduto, nota) => {
    try {
      await axios.post(`${API_BASE_URL}/feedback`, {
        perfil_cliente: formData,
        nome_produto: nomeProduto,
        nota_satisfacao: nota
      });
      setFeedbackSent(prev => ({ ...prev, [nomeProduto]: true }));
    } catch (err) {
      console.error("Erro ao registrar feedback:", err);
    }
  };

  // Reiniciar formulário
  const handleReset = () => {
    setStep(1);
    setFormData({
      curvatura: 3,
      porosidade: 2,
      dano_quimico: 0,
      ressecamento_opacidade: 0,
      alta_porosidade_quimica: 0,
      frizz_falta_definicao: 1,
      transicao_capilar: 0,
      couro_sensivel_oleoso: 0
    });
    setRecommendationResult(null);
    setFeedbackSent({});
    setFeedbackRating({});
    setScreen('welcome');
  };

  return (
    <div className="min-h-screen bg-[#FAF8F5] text-zinc-800 flex flex-col justify-between">
      
      {/* Barra de Topo / Header Institucional */}
      <header className="border-b border-stone-200/80 bg-white/70 backdrop-blur-md px-6 py-4 sticky top-0 z-50">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2.5 cursor-pointer" onClick={handleReset}>
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-stone-800 to-stone-600 flex items-center justify-center text-amber-200 shadow-sm">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-stone-900 font-serif">Vila Cachos</h1>
              <p className="text-xs text-stone-500 font-medium">Totem Inteligente de Diagnóstico Capilar</p>
            </div>
          </div>
          
          {screen !== 'welcome' && (
            <button
              onClick={handleReset}
              className="flex items-center space-x-1.5 text-xs font-semibold text-stone-500 hover:text-stone-800 bg-stone-100 hover:bg-stone-200/80 px-3 py-1.5 rounded-full transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reiniciar</span>
            </button>
          )}
        </div>
      </header>

      {/* Conteúdo Central dinâmico */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-6 flex flex-col justify-center">

        {/* ------------------------------------------------------------- */}
        {/* TELA 1: WELCOME SCREEN                                        */}
        {/* ------------------------------------------------------------- */}
        {screen === 'welcome' && (
          <div className="text-center py-12 px-4 max-w-2xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-stone-100 text-stone-700 text-xs font-semibold mb-6 border border-stone-200">
              <Sparkles className="w-4 h-4 text-amber-600" />
              Sistema Especialista de Recomendação
            </div>
            
            <h2 className="text-4xl md:text-5xl font-extrabold text-stone-900 tracking-tight font-serif mb-6 leading-tight">
              Descubra o produto perfeito para o seu cacho
            </h2>
            
            <p className="text-lg text-stone-600 mb-10 leading-relaxed">
              Em menos de 1 minuto, nossa Inteligência Artificial analisa a estrutura, porosidade e necessidades dos seus fios para recomendar a finalização ideal do nosso catálogo.
            </p>

            <button
              onClick={() => setScreen('anamnese')}
              className="w-full sm:w-auto inline-flex items-center justify-center space-x-3 bg-stone-900 hover:bg-stone-800 text-white font-medium text-lg px-8 py-4 rounded-2xl shadow-xl hover:shadow-2xl transition transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <span>Iniciar Diagnóstico</span>
              <ArrowRight className="w-5 h-5 text-amber-300" />
            </button>

            <div className="mt-14 grid grid-cols-3 gap-4 text-stone-500 text-xs font-medium border-t border-stone-200 pt-8">
              <div>
                <span className="block text-lg font-bold text-stone-800">100%</span>
                Personalizado para você
              </div>
              <div>
                <span className="block text-lg font-bold text-stone-800">Híbrido</span>
                Regras + Satisfação Real
              </div>
              <div>
                <span className="block text-lg font-bold text-stone-800">XAI</span>
                Justificativas Claras
              </div>
            </div>
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* TELA 2: WIZARD DE ANAMNESE                                   */}
        {/* ------------------------------------------------------------- */}
        {screen === 'anamnese' && (
          <div className="bg-white border border-stone-200 rounded-3xl p-6 md:p-10 shadow-sm">
            
            {/* Stepper Superior */}
            <div className="mb-8">
              <div className="flex items-center justify-between text-xs font-semibold text-stone-400 mb-2">
                <span>PASSO {step} DE 4</span>
                <span>
                  {step === 1 && "Curvatura do Fio"}
                  {step === 2 && "Porosidade Capilar"}
                  {step === 3 && "Histórico Químico"}
                  {step === 4 && "Principais Queixas"}
                </span>
              </div>
              <div className="w-full bg-stone-100 h-2 rounded-full overflow-hidden">
                <div 
                  className="bg-stone-900 h-full transition-all duration-300 rounded-full"
                  style={{ width: `${(step / 4) * 100}%` }}
                />
              </div>
            </div>

            {errorMessage && (
              <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-start space-x-2">
                <ShieldAlert className="w-5 h-5 flex-shrink-0 mt-0.5 text-red-600" />
                <span>{errorMessage}</span>
              </div>
            )}

            {/* PASSO 1: Curvatura */}
            {step === 1 && (
              <div>
                <h3 className="text-2xl font-bold text-stone-900 mb-2">Qual é o tipo de curvatura do seu cabelo?</h3>
                <p className="text-stone-500 text-sm mb-6">Selecione o padrão predominante nos seus fios.</p>
                
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {[
                    { val: 2, title: "Tipo 2 - Ondulado", desc: "Ondas em forma de 'S', raiz mais lisa e pontas com movimento suave." },
                    { val: 3, title: "Tipo 3 - Cacheado", desc: "Cachos bem definidos em espiral ou mola, com volume moderado." },
                    { val: 4, title: "Tipo 4 - Crespo", desc: "Curvatura bem fechada em zigue-zague ou molas densas com muito volume." }
                  ].map(item => (
                    <button
                      key={item.val}
                      type="button"
                      onClick={() => handleSelect('curvatura', item.val)}
                      className={`text-left p-5 rounded-2xl border-2 transition relative ${
                        formData.curvatura === item.val
                          ? 'border-stone-900 bg-stone-50/70 shadow-sm'
                          : 'border-stone-200 hover:border-stone-300 bg-white'
                      }`}
                    >
                      {formData.curvatura === item.val && (
                        <div className="absolute top-4 right-4 w-6 h-6 rounded-full bg-stone-900 text-white flex items-center justify-center">
                          <Check className="w-4 h-4" />
                        </div>
                      )}
                      <div className="text-2xl font-extrabold text-stone-900 mb-1">{item.val}</div>
                      <div className="font-bold text-stone-900 mb-1">{item.title}</div>
                      <div className="text-xs text-stone-500 leading-relaxed">{item.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* PASSO 2: Porosidade */}
            {step === 2 && (
              <div>
                <h3 className="text-2xl font-bold text-stone-900 mb-2">Como é a porosidade dos seus fios?</h3>
                <p className="text-stone-500 text-sm mb-6">A porosidade define a capacidade do cabelo de absorver e reter hidratação.</p>
                
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {[
                    { val: 1, title: "Baixa Porosidade", desc: "Cutículas muito fechadas. Demora para molhar e para secar." },
                    { val: 2, title: "Média Porosidade", desc: "Cutículas equilibradas. Absorve e retém tratamentos facilmente." },
                    { val: 3, title: "Alta Porosidade", desc: "Cutículas muito abertas. Absorve água na hora mas resseca rápido." }
                  ].map(item => (
                    <button
                      key={item.val}
                      type="button"
                      onClick={() => handleSelect('porosidade', item.val)}
                      className={`text-left p-5 rounded-2xl border-2 transition relative ${
                        formData.porosidade === item.val
                          ? 'border-stone-900 bg-stone-50/70 shadow-sm'
                          : 'border-stone-200 hover:border-stone-300 bg-white'
                      }`}
                    >
                      {formData.porosidade === item.val && (
                        <div className="absolute top-4 right-4 w-6 h-6 rounded-full bg-stone-900 text-white flex items-center justify-center">
                          <Check className="w-4 h-4" />
                        </div>
                      )}
                      <div className="font-bold text-stone-900 mb-1 text-base">{item.title}</div>
                      <div className="text-xs text-stone-500 leading-relaxed">{item.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* PASSO 3: Dano Químico */}
            {step === 3 && (
              <div>
                <h3 className="text-2xl font-bold text-stone-900 mb-2">Você possui procedimentos químicos nos cabelos?</h3>
                <p className="text-stone-500 text-sm mb-6">Descoloração, luzes, coloração constante ou relaxamentos químicos antigos.</p>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {[
                    { val: 0, title: "Cabelo 100% Natural", desc: "Sem processos de descoloração, tinturas fortes ou alisantes químicos." },
                    { val: 1, title: "Com Química / Descoloração", desc: "Possui luzes, mechas descoloridas, tintura ou químicas de transformação." }
                  ].map(item => (
                    <button
                      key={item.val}
                      type="button"
                      onClick={() => handleSelect('dano_quimico', item.val)}
                      className={`text-left p-6 rounded-2xl border-2 transition relative ${
                        formData.dano_quimico === item.val
                          ? 'border-stone-900 bg-stone-50/70 shadow-sm'
                          : 'border-stone-200 hover:border-stone-300 bg-white'
                      }`}
                    >
                      {formData.dano_quimico === item.val && (
                        <div className="absolute top-4 right-4 w-6 h-6 rounded-full bg-stone-900 text-white flex items-center justify-center">
                          <Check className="w-4 h-4" />
                        </div>
                      )}
                      <div className="font-bold text-stone-900 mb-1 text-lg">{item.title}</div>
                      <div className="text-xs text-stone-500 leading-relaxed">{item.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* PASSO 4: Queixas */}
            {step === 4 && (
              <div>
                <h3 className="text-2xl font-bold text-stone-900 mb-2">Quais queixas mais te incomodam hoje?</h3>
                <p className="text-stone-500 text-sm mb-6">Você pode selecionar mais de uma opção para refinarmos a fórmula exata.</p>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { key: 'ressecamento_opacidade', label: 'Ressecamento e Opacidade', desc: 'Fios ásperos ao toque, sem brilho e precisando de óleos nutritivos.' },
                    { key: 'alta_porosidade_quimica', label: 'Alta Porosidade e Fios Elásticos', desc: 'Pontas espigadas ou elásticas, exigindo acidificação e reconstrução.' },
                    { key: 'frizz_falta_definicao', label: 'Frizz e Falta de Definição', desc: 'Cachos que desmancham no mesmo dia e precisam de fixação forte.' },
                    { key: 'transicao_capilar', label: 'Transição Capilar', desc: 'Duas texturas no mesmo fio, exigindo texturização e alta modelagem.' },
                    { key: 'couro_sensivel_oleoso', label: 'Couro Sensível ou Raiz Oleosa', desc: 'Necessidade de limpeza delicada e fórmulas leves que não pesem.' }
                  ].map(q => {
                    const isChecked = formData[q.key] === 1;
                    return (
                      <div
                        key={q.key}
                        onClick={() => handleToggleQueixa(q.key)}
                        className={`p-4 rounded-2xl border-2 cursor-pointer transition flex items-start space-x-3 ${
                          isChecked 
                            ? 'border-stone-900 bg-stone-50/70 shadow-sm' 
                            : 'border-stone-200 hover:border-stone-300 bg-white'
                        }`}
                      >
                        <div className={`w-5 h-5 rounded-md mt-0.5 flex items-center justify-center border transition ${
                          isChecked ? 'bg-stone-900 border-stone-900 text-white' : 'border-stone-300 bg-white'
                        }`}>
                          {isChecked && <Check className="w-3.5 h-3.5" />}
                        </div>
                        <div className="flex-1">
                          <div className="font-bold text-stone-900 text-sm">{q.label}</div>
                          <div className="text-xs text-stone-500 mt-0.5">{q.desc}</div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Rodapé de Navegação do Wizard */}
            <div className="mt-8 pt-6 border-t border-stone-200 flex items-center justify-between">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={() => setStep(prev => prev - 1)}
                  className="inline-flex items-center space-x-2 text-stone-600 hover:text-stone-900 font-semibold text-sm px-4 py-2.5 rounded-xl transition"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span>Voltar</span>
                </button>
              ) : (
                <button
                  type="button"
                  onClick={() => setScreen('welcome')}
                  className="text-stone-400 hover:text-stone-700 font-semibold text-sm px-4 py-2.5 rounded-xl transition"
                >
                  Cancelar
                </button>
              )}

              {step < 4 ? (
                <button
                  type="button"
                  onClick={() => setStep(prev => prev + 1)}
                  className="inline-flex items-center space-x-2 bg-stone-900 hover:bg-stone-800 text-white font-semibold text-sm px-6 py-3 rounded-xl transition shadow-md hover:shadow-lg"
                >
                  <span>Próximo</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleSubmitAnamnese}
                  className="inline-flex items-center space-x-2 bg-stone-900 hover:bg-stone-800 text-amber-300 font-bold text-sm px-8 py-3.5 rounded-xl transition shadow-xl hover:shadow-2xl transform hover:-translate-y-0.5"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>Gerar Recomendação</span>
                </button>
              )}
            </div>

          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* TELA: LOADING SPINNER                                         */}
        {/* ------------------------------------------------------------- */}
        {screen === 'loading' && (
          <div className="text-center py-20">
            <div className="inline-block w-16 h-16 border-4 border-stone-200 border-t-stone-900 rounded-full animate-spin mb-6" />
            <h3 className="text-2xl font-bold text-stone-900 mb-2">Processando Diagnóstico Capilar...</h3>
            <p className="text-stone-500 text-sm max-w-md mx-auto">
              Calculando compatibilidade terapêutica e aplicando calibração bayesiana dos clusters de clientes do salão.
            </p>
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* TELA 3: RESULTADOS DA RECOMENDAÇÃO                            */}
        {/* ------------------------------------------------------------- */}
        {screen === 'results' && recommendationResult && (
          <div className="space-y-6">
            
            {/* Header de Persona */}
            <div className="bg-white border border-stone-200 rounded-3xl p-6 shadow-sm">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <span className="text-xs font-bold tracking-wider text-amber-700 uppercase bg-amber-50 px-3 py-1 rounded-full border border-amber-200">
                    Persona Identificada no Salão
                  </span>
                  <h3 className="text-xl font-bold text-stone-900 mt-2 font-serif">
                    {recommendationResult.descricao_persona}
                  </h3>
                </div>
                <div className="text-xs text-stone-500 bg-stone-50 p-3 rounded-2xl border border-stone-200/80">
                  <div><strong>Equilíbrio Híbrido:</strong></div>
                  <div>Regras de Conteúdo: {Math.round(recommendationResult.peso_conhecimento_vs_feedback.peso_regras_conteudo * 100)}%</div>
                  <div>Satisfação Coletiva: {Math.round(recommendationResult.peso_conhecimento_vs_feedback.peso_feedback_historico * 100)}%</div>
                </div>
              </div>
            </div>

            {/* Cards do Top 3 Produtos */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {recommendationResult.recomendacoes.map((prod, index) => {
                const isTop1 = index === 0;
                const foiAvaliado = feedbackSent[prod.nome];

                return (
                  <div
                    key={prod.produto_id}
                    className={`bg-white rounded-3xl border transition flex flex-col justify-between overflow-hidden relative ${
                      isTop1 
                        ? 'border-2 border-stone-900 shadow-lg' 
                        : 'border-stone-200 shadow-sm'
                    }`}
                  >
                    {/* Badge do Top 1 */}
                    {isTop1 && (
                      <div className="bg-stone-900 text-amber-300 text-xs font-bold px-4 py-1 text-center flex items-center justify-center space-x-1">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>RECOMENDAÇÃO PRINCIPAL</span>
                      </div>
                    )}

                    <div className="p-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-semibold text-stone-400 uppercase tracking-wider">
                          #{index + 1} {prod.categoria}
                        </span>
                        
                        {/* Estrelas Estimadas */}
                        <div className="flex items-center space-x-1 bg-amber-50 px-2 py-1 rounded-lg border border-amber-200 text-amber-900 text-xs font-bold">
                          <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-500" />
                          <span>{prod.estrelas_estimadas}</span>
                        </div>
                      </div>

                      <h4 className="text-lg font-extrabold text-stone-900 mb-2 leading-snug">
                        {prod.nome}
                      </h4>

                      <p className="text-xs text-stone-600 mb-4 line-clamp-3 leading-relaxed">
                        {prod.descricao}
                      </p>

                      {/* XAI: Justificativa Explicável */}
                      <div className="bg-stone-50 rounded-2xl p-3 border border-stone-200/80 mb-4">
                        <div className="text-[11px] font-bold text-stone-700 flex items-center space-x-1 mb-1">
                          <Info className="w-3.5 h-3.5 text-stone-500" />
                          <span>Por que indicamos?</span>
                        </div>
                        <p className="text-xs text-stone-600 leading-normal">
                          {prod.motivo}
                        </p>
                      </div>
                    </div>

                    {/* Módulo de Feedback Interativo Pós-Atendimento */}
                    <div className="p-4 bg-stone-50/70 border-t border-stone-200 mt-auto">
                      {foiAvaliado ? (
                        <div className="text-center py-2 text-xs font-bold text-emerald-700 flex items-center justify-center space-x-1.5">
                          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                          <span>Obrigado pelo seu feedback!</span>
                        </div>
                      ) : (
                        <div className="text-center">
                          <p className="text-[11px] font-semibold text-stone-500 mb-2">
                            Avalie este produto (Feedback Loop):
                          </p>
                          <div className="flex justify-center items-center space-x-1.5">
                            {[1, 2, 3, 4, 5].map((nota) => (
                              <button
                                key={nota}
                                onClick={() => handleSendFeedback(prod.nome, nota)}
                                className="w-8 h-8 rounded-full bg-white hover:bg-amber-100 border border-stone-200 flex items-center justify-center text-xs font-bold text-stone-700 hover:text-amber-900 transition active:scale-95 shadow-2xs"
                                title={`Dar nota ${nota}`}
                              >
                                {nota}★
                              </button>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                  </div>
                );
              })}
            </div>

            {/* Botão de Finalização */}
            <div className="text-center pt-4">
              <button
                onClick={handleReset}
                className="inline-flex items-center space-x-2 bg-stone-900 hover:bg-stone-800 text-white font-semibold text-sm px-6 py-3 rounded-xl transition shadow-md"
              >
                <RotateCcw className="w-4 h-4" />
                <span>Realizar Novo Diagnóstico</span>
              </button>
            </div>

          </div>
        )}

      </main>

      {/* Footer Discreto */}
      <footer className="border-t border-stone-200/80 bg-white/50 text-stone-400 text-xs py-4 text-center">
        <p>Vila Cachos &copy; 2026 &bull; Sistema Especialista de Recomendação Capilar (TCC)</p>
      </footer>

    </div>
  );
}
