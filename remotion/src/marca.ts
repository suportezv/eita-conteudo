/**
 * Paleta e tokens da EITA Mentora Virtual.
 *
 * Os NOMES das chaves sao herdados do estudio de origem de proposito: Aurora.tsx
 * e CartaoTitulo.tsx sao identicos em todos os estudios irmaos e leem daqui, entao
 * so os hexes mudam de marca para marca. Ler "rosaVivo" como "acento principal".
 *
 * Confirmado: o amarelo #FFE234 e o acento do ecossistema EITA (lettering de video).
 * Sobre a base clara da aurora ele nao tem contraste para texto, entao o destaque
 * do titulo usa o ruivo (cabelo da personagem) e o amarelo entra como mancha.
 * Os demais hexes sao PROVISORIOS ate a marca fechar identidade visual propria.
 */
export const marca = {
  /** Acento principal: ruivo da EITA. Destaque do titulo e mancha quente. */
  rosaVivo: "#D9532B",
  /** Ruivo profundo, para apoio e sombra. */
  rosa: "#B23E1C",
  /** Amarelo EITA #FFE234, o acento confirmado do ecossistema. */
  rosaSuave: "#FFE234",
  /** Ambar: ponte entre o ruivo e o amarelo na aurora. */
  violeta: "#F2A03D",
  /** Verde acolhida: a nota calma que equilibra o calor. */
  ciano: "#3FB59B",
  azulNeon: "#7FD8C6",
  azulProfundo: "#2E5A52",
  fundoEscuro: "#14100A",
  superficie: "#241D14",
  /** Base clara e quente dos fundos aurora. */
  auroraBase: "#FFF8EC",
  tinta: "#241D14",
  /** Sem rede de fontes no render headless: cai para a sans do sistema. */
  fonte: '"Inter Tight", system-ui, -apple-system, sans-serif',
} as const;
