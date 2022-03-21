%%
% Question 1
 I = imread('baboon.bmp');
 %imshow(I);
 disp(size(I));
 
 ker1 = 0.04*ones(5,5);
 result = conv2(I,ker1,"same");
 disp(size(result));
 
 imshow(result,[]);

 %%
 % Question2
Result2 = awgn(result,10,"measured");
imshow(Result2,[]);

 %%
 % Question3
 NSR = (-10/10)^10;
 wnr1 = deconvwnr(Result2, ker1, NSR);
 imshow(wnr1,[]);

 %%
 % Another Try
 noise = Result2 - result;
 estimated_nsr = var(noise(:)) / var(Result2(:));
 wnr2 = deconvwnr(Result2, ker1, estimated_nsr);
 imshow(wnr2,[]);

 %%
 % Deconvoluntion FFT
 F = fft2(Result2);
 F  =fftshift(F);
 H = fft2(ker1,512,512);
 H = fftshift(H);

 F = F./H;
 X = ifftshift(F);
 x = ifft2(X);

 %imshow(F,[]);
 imshow(x,[]);

 
 

















