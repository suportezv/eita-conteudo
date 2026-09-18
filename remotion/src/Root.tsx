import React from "react";
import { Composition } from "remotion";
import { CartaoTitulo } from "./CartaoTitulo";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="CartaoTituloVertical"
      component={CartaoTitulo}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        titulo: "Respira. A EITA fica com você agora",
        destaque: "EITA",
        rodape: "@eita.mentoravirtual",
      }}
    />
    <Composition
      id="CartaoTituloQuadrado"
      component={CartaoTitulo}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{
        titulo: "Respira. A EITA fica com você agora",
        destaque: "EITA",
        rodape: "@eita.mentoravirtual",
      }}
    />
  </>
);
