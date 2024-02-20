/*  ------------------------------------------------------------------
    Copyright (c) 2011-2020 Marc Toussaint
    email: toussaint@tu-berlin.de

    This code is distributed under the MIT License.
    Please see <root-path>/LICENSE for details.
    --------------------------------------------------------------  */

#pragma once

#include "kin.h"
#include "proxy.h"

namespace rai {

struct ConfigurationViewer : GLDrawer {
  ~ConfigurationViewer();

  int setConfiguration(const Configuration& _C, const char* text=0, bool watch=false);
  int setPath(ConfigurationL& Cs, const char* text=0, bool watch=false);
  int setPath(rai::Configuration& _C, const arr& jointPath, const char* text=0, bool watch=false, bool full=true);
  int setPath(const arr& _framePath, const char* text=0, bool watch=false, bool full=true);
  bool playVideo(uint T, uint nFrames, bool watch=true, double delay=1., const char* saveVideoPath=nullptr); ///< display the trajectory; use "z.vid/" as vid prefix
  bool playVideo(bool watch=true, double delay=1., const char* saveVideoPath=nullptr); ///< display the trajectory; use "z.vid/" as vid prefix
  rai::Camera& displayCamera();   ///< access to the display camera to change the view
  byteA getRgb();
  floatA getDepth();
  void savePng(const char* saveVideoPath="z.vid/");
  void recopyMeshes(const Configuration& _C);

  rai::Configuration& getConfiguration(){ return C; }


  int update(bool watch=false);
  void raiseWindow();
  void glDraw(OpenGL&);
  OpenGL& ensure_gl();
  void setCamera(rai::Frame* cam);

  //mimic a OpenGL, directly calling the same methods in its gl
  int update(const char* text=nullptr, bool nonThreaded=false);
  int watch(const char* text=nullptr);
  void add(GLDrawer& c);
  void resetPressedKey();
  void clear();

private://draw data
  Configuration C;

  arr framePath;
  FrameL drawSubFrames;
  int drawTimeSlice;
  bool drawFullPath;
  int tprefix;
  bool writeToFiles;
  uint pngCount=0;
public:
  String drawText;
  shared_ptr<struct OpenGL> gl;
  bool drawFrameLines=true;
  double phaseOffset=0., phaseFactor=-1.;
};

}
