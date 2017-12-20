import LocalizedStrings from 'react-localization';

let sentences = new LocalizedStrings({
  en:{
    signIn:"sign-in",
    signOut:"sign-up",
    languages:"Languages",
    fonts:"Fonts",
    profile:"Perfil",
    UserCreations:"User creations",
    PostReports:"Post reports",
    search:"Search",
  },
  es: {
    signIn:"Iniciar sesión",
    signOut:"Cerrar sesión",
    languages:"Idiomas",
    fonts:"Fuentes",
    profile:"Perfil",
    UserCreations:"Solicitud de nuevos usuarios",
    PostReports:"Publicaciones reportadas",
    search:"Buscar",
  }
});

export default sentences;