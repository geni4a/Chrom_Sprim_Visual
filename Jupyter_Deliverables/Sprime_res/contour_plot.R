# plot match rate to Neanderthal vs Denisovan
library(MASS)
pdf("NDcontour.pdf",width=15,height=12); minn=10; zoom=F; xlab="Match to Altai Neanderthal"; ylab="Match to Altai Denisovan"; level1=seq(0.3,0.9,0.1); level2=seq(1,30,1)
par(mfrow=c(4,5),mar=c(5,5,4,1)+0.1)
pops=c("CEU","FIN","GBR","IBS","TSI","CDX","CHB","CHS","JPT","KHV","BEB","GIH","ITU","PJL","STU","MXL","PUR","CLM","PEL","Papuans")
popnames=c("NW European (Utah)","Finnish","British","Iberian (Spain)","Toscani (Italy)","Chinese Dai","Han Chinese (Beijing)","Southern Han Chinese","Japanese (Tokyo)","Kinh (Vietnam)","Bengali (Bangladesh)","Gujarati Indian (Houston)","Indian Telugu (UK)","Punjabi (Pakistan)","Sri Lankan Tamil (UK)","Mexican (Los Angeles)","Puerto Rican","Colombian","Peruvian","Papuan")
for(i in 1:length(pops)){
pop = pops[i]
popname = popnames[i]
allmatch=c()
for(chr in 1:22){
  x=read.table(paste(pop,".chr",chr,".ND_match",sep=""),header=T)  
  segmentids = unique(x$SEGMENT)
  matching = sapply(segmentids,function(s){
    z=x[x$SEGMENT==s,]
    nmatch1=sum(z$NMATCH=="match")
    nmatch2=sum(z$DMATCH=="match")
    nmis1=sum(z$NMATCH=="mismatch")
    nmis2=sum(z$DMATCH=="mismatch")
    if(nmatch1+nmis1>=minn & nmatch2+nmis2>=minn){return(c(nmatch1/(nmatch1+nmis1),nmatch2/(nmatch2+nmis2)))}else{return(c(-1,-1))}
  })
  allmatch=cbind(allmatch,matching[,matching[1,]>=0])
}
contour(kde2d(allmatch[1,],allmatch[2,],lims=c(0,1,0,1),n=100),xaxs="i",yaxs="i",xlab=xlab,ylab=ylab,main=popname,levels=level1,las=1,cex.lab=1.5,cex.axis=1.4,cex.main=1.5,lty=5,labcex=0.8);abline(h=seq(0.2,0.8,0.2),v=seq(0.2,0.8,0.2),lty=3,col="gray")
contour(kde2d(allmatch[1,],allmatch[2,],lims=c(0,1,0,1),n=100),xaxs="i",yaxs="i",xlab=xlab,ylab=ylab,main=popname,levels=level2,las=1,cex.lab=1.5,cex.axis=1.4,cex.main=1.5,labcex=0.8,add=T);abline(h=seq(0.2,0.8,0.2),v=seq(0.2,0.8,0.2),lty=3,col="gray")
}
dev.off()
