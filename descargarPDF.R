setwd("~/Dropbox/Cuentas claras Plebiscito 2016")
for( i in 1550:1654 ){
fileurl<-paste("www5.registraduria.gov.co/PlebiscitoPublico2016/Consultas/Organizacion/Formulario51pdf/",i,sep="")  
file<-paste("./","Formulario contribuciones o donaciones de los particulares",i,".pdf", sep = "")
download.file(fileurl,destfile=file)
}
