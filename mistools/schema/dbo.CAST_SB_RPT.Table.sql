DROP TABLE [dbo].[CAST_SB_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_SB_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_SB_RPT](
	[CAST_SB_RPT_ID] [int] NOT NULL,
	[CAST_SB_RPT_FLAG] [bit] NOT NULL,
	[CAST_SB_WORK_ID] [varchar](10) NULL,
	[CASTSB_STUDENT_ID] [varchar](10) NULL,
	[CASTSB_GI03] [varchar](3) NULL,
	[CASTSB_GI01] [varchar](3) NULL,
	[CASTSB_SB00] [varchar](10) NULL,
	[CASTSB_SB01] [varchar](1) NULL,
	[CASTSB_SB02] [varchar](3) NULL,
	[CASTSB_SB03] [varchar](8) NULL,
	[CASTSB_SB04] [varchar](1) NULL,
	[CASTSB_SB05] [varchar](2) NULL,
	[CASTSB_SB06] [varchar](1) NULL,
	[CASTSB_SB08] [varchar](9) NULL,
	[CASTSB_SB09] [varchar](5) NULL,
	[CASTSB_SB11] [varchar](5) NULL,
	[CASTSB_SB12] [varchar](6) NULL,
	[CASTSB_SB14] [varchar](1) NULL,
	[CASTSB_SB15] [varchar](1) NULL,
	[CASTSB_SB16] [varchar](6) NULL,
	[CASTSB_SB17] [varchar](6) NULL,
	[CASTSB_SB18] [varchar](6) NULL,
	[CASTSB_SB19] [varchar](6) NULL,
	[CASTSB_SB20] [varchar](6) NULL,
	[CASTSB_SB21] [varchar](6) NULL,
	[CASTSB_SB22] [varchar](1) NULL,
	[CASTSB_SB23] [varchar](1) NULL,
	[CASTSB_SB24] [varchar](1) NULL,
	[CASTSB_SB26] [varchar](1) NULL,
	[CASTSB_SB27] [varchar](1) NULL,
	[CASTSB_SB28] [varchar](3) NULL,
	[CASTSB_KEY_IDX] [varchar](18) NULL,
	[CASTSB_SB29] [varchar](21) NULL,
	[CASTSB_SB30] [varchar](1) NULL,
	[CASTSB_SB31] [varchar](30) NULL,
	[CASTSB_SB32] [varchar](40) NULL,
	[CASTSB_SB33] [varchar](2) NULL,
	[CASTSB_SB34] [varchar](8) NULL,
	[CASTSB_SB35] [varchar](10) NULL,
	[CASTSB_SB36] [varchar](1) NULL,
	[CASTSB_SB37] [varchar](1) NULL,
	[CAST_SB_WORK_ADDDATE] [datetime] NULL,
	[CAST_SB_WORK_ADDOPR] [varchar](20) NULL,
	[CAST_SB_WORK_CHGDATE] [datetime] NULL,
	[CAST_SB_WORK_CHGOPR] [varchar](20) NULL,
	[CASTSB_SB39A] [varchar](1) NULL,
	[CASTSB_SB39B] [varchar](1) NULL,
 CONSTRAINT [PK_SB_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_SB_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_SB_R__CAST___4000A096]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_SB_RPT] ADD  DEFAULT ((1)) FOR [CAST_SB_RPT_FLAG]
END
GO
