import LocalizedStrings from 'react-localization';

let sentences = new LocalizedStrings({
  en:{
    signIn:"sign-in",
    signOut:"sign-up",
    languages:"Languages",
    fonts:"Fonts",
    profile:"Perfil",
    newUsers:"User creations",
    reportedPosts:"Post reports",
    search:"Search",
  },
  es: {
    signIn:"Iniciar sesión",
    signOut:"Cerrar sesión",
    languages:"Idiomas",
    fonts:"Fuentes",
    profile:"Perfil",
    newUsers:"Solicitud de nuevos usuarios",
    reportedPosts:"Publicaciones reportadas",
    search:"Buscar",
  }
});

export default sentences;